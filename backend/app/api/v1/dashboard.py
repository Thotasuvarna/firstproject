"""
Dashboard Metrics & Threat Intelligence Overview Endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.product import Product
from app.models.reviewer import Reviewer
from app.models.review import Review
from app.models.analysis import ReviewAnalysis
from app.models.cluster import CollusionCluster
from app.schemas.report import DashboardMetricsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/metrics", response_model=DashboardMetricsResponse)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Computes high-level security metrics, threat statistics, and risk tiers."""
    total_reviews = db.query(Review).count()
    total_products = db.query(Product).count()
    total_reviewers = db.query(Reviewer).count()
    detected_clusters_count = db.query(CollusionCluster).count()

    # Risk tier breakdown
    high_count = db.query(ReviewAnalysis).filter(ReviewAnalysis.risk_tier == "HIGH").count()
    medium_count = db.query(ReviewAnalysis).filter(ReviewAnalysis.risk_tier == "MEDIUM").count()
    low_count = db.query(ReviewAnalysis).filter(ReviewAnalysis.risk_tier == "LOW").count()

    suspicious_count = high_count + medium_count
    suspicious_percentage = round((suspicious_count / max(total_reviews, 1)) * 100.0, 1)

    # Average Trust Score
    avg_trust = db.query(func.avg(Product.product_trust_score)).scalar() or 100.0

    # Top flagged products (lowest trust score)
    top_flagged_products = (
        db.query(Product)
        .order_by(Product.product_trust_score.asc())
        .limit(5)
        .all()
    )
    products_out = [
        {
            "id": p.id,
            "sku": p.product_sku,
            "title": p.title,
            "trust_score": p.product_trust_score,
            "total_reviews": p.total_reviews,
            "avg_rating": p.average_rating
        }
        for p in top_flagged_products
    ]

    # Recent suspicious reviews
    recent_suspicious = (
        db.query(Review, ReviewAnalysis, Product)
        .join(ReviewAnalysis, Review.id == ReviewAnalysis.review_id)
        .join(Product, Review.product_id == Product.id)
        .filter(ReviewAnalysis.risk_tier.in_(["HIGH", "MEDIUM"]))
        .order_by(ReviewAnalysis.composite_suspicion_score.desc())
        .limit(8)
        .all()
    )
    
    recent_out = []
    for rev, analysis, prod in recent_suspicious:
        # Extract primary reason from explainability factors
        reasons = analysis.explainability_factors.get("primary_drivers", []) if analysis.explainability_factors else []
        top_reason = reasons[0]["description"] if reasons else "Elevated linguistic & behavioral anomaly"
        
        recent_out.append({
            "review_id": rev.id,
            "product_sku": prod.product_sku,
            "rating": rev.rating,
            "composite_suspicion_score": analysis.composite_suspicion_score,
            "risk_tier": analysis.risk_tier,
            "top_reason": top_reason,
            "snippet": rev.review_text[:120] + ("..." if len(rev.review_text) > 120 else "")
        })

    return {
        "total_reviews": total_reviews,
        "suspicious_reviews_count": suspicious_count,
        "suspicious_reviews_percentage": suspicious_percentage,
        "total_products": total_products,
        "total_reviewers": total_reviewers,
        "detected_clusters_count": detected_clusters_count,
        "average_trust_score": round(float(avg_trust), 1),
        "risk_tier_breakdown": {
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        },
        "top_flagged_products": products_out,
        "recent_suspicious_reviews": recent_out
    }
