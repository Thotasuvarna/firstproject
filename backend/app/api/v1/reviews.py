"""
Review Ingestion & Query Endpoints.
Integrates automated NLP, behavioral profiling, and Explainable AI risk scoring.
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session
import csv
import io

from app.core.database import get_db
from app.core.security import pseudonymize_reviewer_id
from app.models.product import Product
from app.models.reviewer import Reviewer
from app.models.review import Review
from app.models.analysis import ReviewAnalysis
from app.schemas.review import ReviewCreate, ReviewBatchUpload, ReviewResponse
from app.services.nlp_service import nlp_service
from app.services.behavioral_service import behavioral_service
from app.services.ml_service import ml_service
from app.services.scoring_service import scoring_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


def process_and_save_review(
    review_in: ReviewCreate,
    db: Session
) -> Review:
    """Core pipeline function that ingests, scores, and stores a review."""
    # 1. Verify or create Product
    product = db.query(Product).filter(Product.product_sku == review_in.product_sku).first()
    if not product:
        product = Product(
            product_sku=review_in.product_sku,
            title=f"Product {review_in.product_sku}",
            category="Imported",
            average_rating=review_in.rating,
            total_reviews=1,
            product_trust_score=100.0
        )
        db.add(product)
        db.flush()

    # 2. Anonymize reviewer identity (salted SHA-256)
    reviewer_hash = pseudonymize_reviewer_id(review_in.reviewer_identifier)
    reviewer = db.query(Reviewer).filter(Reviewer.reviewer_hash == reviewer_hash).first()
    
    review_date = review_in.review_date or datetime.now(timezone.utc)
    if review_date.tzinfo is not None:
        review_date = review_date.replace(tzinfo=None)

    if not reviewer:
        reviewer = Reviewer(
            reviewer_hash=reviewer_hash,
            display_alias=f"User_{reviewer_hash[:8]}",
            total_reviews_count=1,
            avg_rating_given=review_in.rating,
            anomaly_score=0.0,
            first_seen=review_date,
            last_seen=review_date
        )
        db.add(reviewer)
        db.flush()
    else:
        # Update reviewer stats
        reviewer.total_reviews_count += 1
        reviewer.avg_rating_given = round(
            (reviewer.avg_rating_given * (reviewer.total_reviews_count - 1) + review_in.rating) / reviewer.total_reviews_count, 
            2
        )
        last_seen = reviewer.last_seen
        if last_seen and last_seen.tzinfo is not None:
            last_seen = last_seen.replace(tzinfo=None)
        if last_seen is None or review_date > last_seen:
            reviewer.last_seen = review_date

    # 3. Create Review Record
    review = Review(
        product_id=product.id,
        reviewer_id=reviewer.id,
        rating=review_in.rating,
        review_title=review_in.review_title or "",
        review_text=review_in.review_text,
        review_date=review_date,
        is_verified_purchase=bool(review_in.is_verified_purchase)
    )
    db.add(review)
    db.flush()

    # 4. Pipeline Analysis: NLP & Duplicate Matching
    # Fetch recent reviews to compare similarity
    corpus_reviews = db.query(Review.review_text).filter(Review.id != review.id).order_by(Review.id.desc()).limit(200).all()
    corpus_texts = [r[0] for r in corpus_reviews if r[0]]
    
    dup_sim, _ = nlp_service.calculate_duplicate_similarity(review.review_text, corpus_texts)
    sentiment = nlp_service.calculate_sentiment(review.review_text)
    sentiment_divergence = nlp_service.calculate_rating_divergence(review.rating, sentiment)

    # 5. Pipeline Analysis: Behavioral & ML Inference
    reviewer_dates = [r.review_date for r in reviewer.reviews] + [review_date]
    burst_velocity = behavioral_service.calculate_velocity_anomaly(reviewer_dates)
    reviewer_ratings = [r.rating for r in reviewer.reviews] + [review.rating]
    extremity = behavioral_service.calculate_rating_extremity(reviewer_ratings)

    ml_prob = ml_service.predict_deception_probability(
        review_text=review.review_text,
        rating=review.rating,
        is_verified_purchase=review.is_verified_purchase
    )

    # 6. Composite Explainable Scoring
    suspicion_score, risk_tier, explainability = scoring_service.compute_composite_score(
        duplicate_similarity=dup_sim,
        sentiment_divergence=sentiment_divergence,
        burst_velocity=burst_velocity,
        rating_extremity=extremity,
        is_verified_purchase=review.is_verified_purchase,
        ml_prob=ml_prob,
        is_in_collusion_cluster=False  # Updated by graph batch job
    )

    # 7. Save Analysis
    analysis = ReviewAnalysis(
        review_id=review.id,
        duplicate_similarity_score=dup_sim,
        sentiment_polarity=sentiment,
        rating_divergence_score=sentiment_divergence,
        ml_prediction_prob=round(suspicion_score / 100.0, 3),
        composite_suspicion_score=suspicion_score,
        risk_tier=risk_tier,
        explainability_factors=explainability,
        analyzed_at=datetime.now(timezone.utc)
    )
    db.add(analysis)

    # 8. Update Product Aggregate Stats
    all_prod_reviews = db.query(Review).filter(Review.product_id == product.id).all()
    product.total_reviews = len(all_prod_reviews)
    product.average_rating = round(sum(r.rating for r in all_prod_reviews) / len(all_prod_reviews), 2)
    
    # Dampen trust score based on average suspicion
    all_prod_analyses = db.query(ReviewAnalysis).join(Review).filter(Review.product_id == product.id).all()
    if all_prod_analyses:
        avg_suspicion = sum(a.composite_suspicion_score for a in all_prod_analyses) / len(all_prod_analyses)
        product.product_trust_score = round(max(0.0, 100.0 - avg_suspicion), 1)

    return review


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def submit_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Submits a single review, executes real-time AI analysis, and saves record."""
    review = process_and_save_review(review_in, db)
    db.commit()
    db.refresh(review)
    return review


@router.post("/batch", status_code=status.HTTP_201_CREATED)
def batch_upload_reviews(
    batch: ReviewBatchUpload,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Batch ingests a JSON list of reviews and processes them sequentially."""
    created_ids = []
    for r in batch.reviews:
        review = process_and_save_review(r, db)
        created_ids.append(review.id)
    db.commit()
    return {"message": f"Successfully ingested and analyzed {len(created_ids)} reviews", "review_ids": created_ids}


@router.post("/upload-csv")
def upload_csv_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Parses an uploaded CSV file containing product reviews.
    Required columns: product_sku, reviewer_identifier, rating, review_text
    Optional columns: review_title, review_date, is_verified_purchase
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV format")

    content = file.file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    
    count = 0
    for row in reader:
        try:
            sku = row.get("product_sku") or row.get("asin") or row.get("product_id", "GENERIC_SKU")
            rev_id = row.get("reviewer_identifier") or row.get("reviewerID") or row.get("user_id", "anon")
            rating = float(row.get("rating") or row.get("overall", 5.0))
            text = row.get("review_text") or row.get("reviewText") or row.get("text", "")
            title = row.get("review_title") or row.get("summary", "")
            verified = str(row.get("is_verified_purchase") or row.get("verified", "false")).lower() in ["true", "1", "yes"]

            review_in = ReviewCreate(
                product_sku=sku,
                reviewer_identifier=rev_id,
                rating=rating,
                review_title=title,
                review_text=text,
                is_verified_purchase=verified
            )
            process_and_save_review(review_in, db)
            count += 1
        except Exception:
            continue

    db.commit()
    return {"message": f"Successfully imported and analyzed {count} reviews from CSV"}


@router.get("", response_model=List[ReviewResponse])
def list_reviews(
    product_sku: Optional[str] = None,
    risk_tier: Optional[str] = None,
    min_score: Optional[float] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Lists reviews with optional filters for product, risk tier, or minimum suspicion score."""
    query = db.query(Review).join(ReviewAnalysis)
    
    if product_sku:
        query = query.join(Product).filter(Product.product_sku == product_sku)
    if risk_tier:
        query = query.filter(ReviewAnalysis.risk_tier == risk_tier.upper())
    if min_score is not None:
        query = query.filter(ReviewAnalysis.composite_suspicion_score >= min_score)

    return query.order_by(Review.id.desc()).offset(skip).limit(limit).all()
