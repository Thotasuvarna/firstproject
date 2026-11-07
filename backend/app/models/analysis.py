"""
Review Analysis ORM model.
Stores NLP, ML prediction, behavioral scores, and Explainable AI (XAI) factors.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class ReviewAnalysis(Base):
    __tablename__ = "review_analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    duplicate_similarity_score = Column(Float, default=0.0, nullable=False)  # 0 to 1.0
    sentiment_polarity = Column(Float, default=0.0, nullable=False)  # -1.0 to 1.0
    rating_divergence_score = Column(Float, default=0.0, nullable=False)  # 0 to 1.0
    ml_prediction_prob = Column(Float, default=0.0, nullable=False)  # 0 to 1.0
    composite_suspicion_score = Column(Float, default=0.0, nullable=False)  # 0 to 100
    risk_tier = Column(String(20), default="LOW", nullable=False)  # 'LOW', 'MEDIUM', 'HIGH'
    explainability_factors = Column(JSON, nullable=True)
    analyzed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    review = relationship("Review", back_populates="analysis")
