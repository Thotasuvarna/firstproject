"""
Review ORM model.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Float, nullable=False)
    review_title = Column(String(255), default="", nullable=False)
    review_text = Column(Text, nullable=False)
    review_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    is_verified_purchase = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="reviews")
    reviewer = relationship("Reviewer", back_populates="reviews")
    analysis = relationship("ReviewAnalysis", uselist=False, back_populates="review", cascade="all, delete-orphan")
