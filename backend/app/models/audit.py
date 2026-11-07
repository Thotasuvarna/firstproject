"""
Audit Log ORM model.
Maintains an immutable chain of human-in-the-loop audit decisions and actions.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action_type = Column(String(50), nullable=False)  # 'VERIFIED_FLAG', 'DISMISSED_FLAG', 'EXPORTED_REPORT'
    target_entity = Column(String(50), nullable=False)  # 'REVIEW', 'CLUSTER', 'PRODUCT'
    target_id = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
