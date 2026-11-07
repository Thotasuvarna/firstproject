"""
Collusion Cluster & Membership ORM models.
Tracks detected reviewer rings and graph community memberships.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CollusionCluster(Base):
    __tablename__ = "collusion_clusters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cluster_name = Column(String(100), unique=True, index=True, nullable=False)
    collusion_density = Column(Float, default=0.0, nullable=False)  # Graph edge density (0 to 1)
    member_count = Column(Integer, default=0, nullable=False)
    co_reviewed_products_count = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="DETECTED", nullable=False)  # 'DETECTED', 'AUDITED', 'DISMISSED'
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    memberships = relationship("ClusterMembership", back_populates="cluster", cascade="all, delete-orphan")


class ClusterMembership(Base):
    __tablename__ = "cluster_memberships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cluster_id = Column(Integer, ForeignKey("collusion_clusters.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id", ondelete="CASCADE"), nullable=False, index=True)
    centrality_score = Column(Float, default=0.0, nullable=False)  # Betweenness / Degree centrality
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    cluster = relationship("CollusionCluster", back_populates="memberships")
    reviewer = relationship("Reviewer", back_populates="cluster_memberships")
