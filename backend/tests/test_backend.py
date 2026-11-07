"""
Comprehensive Test Suite for AI Fake Review & Network Detection System.
Tests Database Models, Auth, NLP, Graph Theory, Scoring, and API Workflow.
"""
import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import pseudonymize_reviewer_id, hash_password, verify_password, create_access_token, decode_access_token
from app.services.nlp_service import nlp_service
from app.services.graph_service import graph_service
from app.services.scoring_service import scoring_service
from app.services.report_service import report_service
from app.models.user import User
from app.models.product import Product
from app.models.review import Review
from app.models.analysis import ReviewAnalysis

from app.api.v1.auth import login, register
from app.schemas.auth import UserRegister
from app.api.v1.products import create_product, list_products
from app.schemas.product import ProductCreate
from app.api.v1.reviews import submit_review, list_reviews
from app.schemas.review import ReviewCreate
from app.api.v1.dashboard import get_dashboard_metrics
from app.api.v1.graph import get_network_graph

# Setup isolated in-memory test database
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def db():
    """Provides a transactional database session per test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_pseudonymization_privacy():
    """Verify reviewer email/username is pseudonymized into salted hash."""
    email1 = "spammer@collusion-farm.org"
    email2 = "spammer@collusion-farm.org"
    email3 = "legit.user@gmail.com"

    hash1 = pseudonymize_reviewer_id(email1)
    hash2 = pseudonymize_reviewer_id(email2)
    hash3 = pseudonymize_reviewer_id(email3)

    assert hash1 == hash2, "Deterministic hash must match for identical identifier"
    assert hash1 != hash3, "Different users must produce different hashes"
    assert email1 not in hash1, "Original identity must never appear in hash"
    assert len(hash1) == 24


def test_password_hashing_and_jwt():
    """Verify password bcrypt hashing and JWT token claims."""
    raw_pw = "SuperSecurePassword99!"
    hashed = hash_password(raw_pw)
    assert verify_password(raw_pw, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

    token = create_access_token(subject=42, role="admin")
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "42"
    assert decoded["role"] == "admin"


def test_public_registration_grants_analyst_access(db):
    """Public signups can access analyst workflows but cannot grant themselves admin."""
    register(
        UserRegister(
            email="bootstrap.admin@example.test",
            password="BootstrapPass1",
            full_name="Bootstrap Admin"
        ),
        db=db
    )

    user = register(
        UserRegister(
            email="public.analyst@example.test",
            password="AnalystPass1",
            full_name="Public Analyst",
            role="admin"
        ),
        db=db
    )

    assert user.role == "analyst"
    token = login(
        form_data=OAuth2PasswordRequestForm(
            username=user.email,
            password="AnalystPass1"
        ),
        db=db
    )
    assert token["role"] == "analyst"


@pytest.mark.parametrize("password", ["x" * 73, "🙂" * 19])
def test_registration_rejects_password_over_bcrypt_byte_limit(password):
    """Reject passwords bcrypt cannot hash before registration reaches the endpoint."""
    with pytest.raises(ValueError, match="72 UTF-8 bytes"):
        UserRegister(
            email="long.password@example.test",
            password=password,
            full_name="Long Password"
        )


def test_nlp_duplicate_and_sentiment():
    """Test TF-IDF Cosine Similarity and sentiment divergence."""
    corpus = [
        "This product is absolutely amazing, best purchase of the year!",
        "Shipping was fast and customer service was helpful.",
        "Terrible quality, broke after two days."
    ]
    target_duplicate = "This product is absolutely amazing, best purchase of the year!"
    sim, matched = nlp_service.calculate_duplicate_similarity(target_duplicate, corpus)
    assert sim >= 0.95, f"Expected near 1.0 similarity for duplicate, got {sim}"

    target_unique = "The blue widget has ergonomic grips and USB-C connectivity."
    sim_unique, _ = nlp_service.calculate_duplicate_similarity(target_unique, corpus)
    assert sim_unique < 0.50

    pos_sent = nlp_service.calculate_sentiment("Outstanding, excellent, love it!")
    neg_sent = nlp_service.calculate_sentiment("Awful, terrible, horrible waste of money.")
    assert pos_sent > 0.0
    assert neg_sent < 0.0

    div = nlp_service.calculate_rating_divergence(5.0, -0.8)
    assert div > 0.6, f"Expected high divergence for 5 stars with negative sentiment, got {div}"


def test_graph_network_collusion_mining():
    """Test NetworkX bipartite graph and clique detection."""
    records = [
        {"reviewer_id": 101, "reviewer_alias": "Rev_A", "product_id": 501, "product_title": "Prod_1", "rating": 5.0, "suspicion_score": 75.0},
        {"reviewer_id": 102, "reviewer_alias": "Rev_B", "product_id": 501, "product_title": "Prod_1", "rating": 5.0, "suspicion_score": 80.0},
        {"reviewer_id": 103, "reviewer_alias": "Rev_C", "product_id": 501, "product_title": "Prod_1", "rating": 5.0, "suspicion_score": 70.0},
        {"reviewer_id": 101, "reviewer_alias": "Rev_A", "product_id": 502, "product_title": "Prod_2", "rating": 5.0, "suspicion_score": 75.0},
        {"reviewer_id": 102, "reviewer_alias": "Rev_B", "product_id": 502, "product_title": "Prod_2", "rating": 5.0, "suspicion_score": 80.0},
        {"reviewer_id": 103, "reviewer_alias": "Rev_C", "product_id": 502, "product_title": "Prod_2", "rating": 5.0, "suspicion_score": 70.0},
    ]

    B = graph_service.build_bipartite_graph(records)
    assert B.number_of_nodes() == 5
    assert B.number_of_edges() == 6

    co_graph = graph_service.project_co_review_graph(B, min_shared_products=1)
    assert co_graph.number_of_nodes() == 3
    
    clusters = graph_service.detect_collusion_clusters(co_graph, min_cluster_size=2)
    assert len(clusters) >= 1
    assert clusters[0]["member_count"] == 3
    assert clusters[0]["density"] >= 0.9


def test_explainable_scoring():
    """Test composite scoring and explainability factors."""
    score, tier, exp = scoring_service.compute_composite_score(
        duplicate_similarity=0.92,
        sentiment_divergence=0.85,
        burst_velocity=0.80,
        rating_extremity=1.0,
        is_verified_purchase=False,
        is_in_collusion_cluster=True,
        cluster_density=0.85
    )
    assert score >= 70.0
    assert tier == "HIGH"
    assert len(exp["primary_drivers"]) >= 3
    assert exp["component_breakdown"]["is_unverified"] is True


def test_api_workflow_end_to_end(db):
    """Test complete API business workflow with persistence."""
    # 1. Register User
    user = register(
        UserRegister(
            email="lead.analyst@gmail.com",
            password="SecurePassword123!",
            full_name="Lead Trust Analyst",
            role="admin"
        ),
        db=db
    )
    assert user.id is not None
    assert user.email == "lead.analyst@gmail.com"

    # 2. Create Product
    product = create_product(
        ProductCreate(
            product_sku="TECH-SMART-99",
            title="Quantum 5G Smartphone",
            category="Electronics",
            description="Flagship smartphone device"
        ),
        db=db,
        current_user=user
    )
    assert product.id is not None

    # 3. Submit Suspicious Review
    review = submit_review(
        ReviewCreate(
            product_sku="TECH-SMART-99",
            reviewer_identifier="bot_collusion_network@darknet.org",
            rating=5.0,
            review_title="Must Buy!",
            review_text="Horrible terrible broke immediately, awful useless garbage scam!",
            is_verified_purchase=False
        ),
        db=db,
        current_user=user
    )
    assert review.id is not None
    assert review.analysis is not None
    assert review.analysis.risk_tier in ["MEDIUM", "HIGH"]
    assert review.analysis.rating_divergence_score > 0.5

    # 4. Dashboard Metrics Verification
    metrics = get_dashboard_metrics(db=db)
    assert metrics["total_reviews"] >= 1
    assert metrics["total_products"] >= 1
    assert metrics["suspicious_reviews_count"] >= 1


def test_pdf_report_generation(db):
    """Test PDF forensic dossier compilation."""
    metrics = get_dashboard_metrics(db=db)
    pdf_buffer = report_service.generate_audit_dossier(metrics)
    assert pdf_buffer is not None
    pdf_bytes = pdf_buffer.getvalue()
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")
