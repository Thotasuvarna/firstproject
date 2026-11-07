"""
Reviewer ORM model.
Uses hashed identifiers to protect reviewer privacy while tracking behavior.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reviewer(Base):
    __tablename__ = "reviewers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewer_hash = Column(String(64), unique=True, index=True, nullable=False)
    display_alias = Column(String(100), nullable=False)
    total_reviews_count = Column(Integer, default=1, nullable=False)
    avg_rating_given = Column(Float, default=0.0, nullable=False)
    anomaly_score = Column(Float, default=0.0, nullable=False)  # 0 to 100
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    reviews = relationship("Review", back_populates="reviewer", cascade="all, delete-orphan")
    cluster_memberships = relationship("ClusterMembership", back_populates="reviewer", cascade="all, delete-orphan")
