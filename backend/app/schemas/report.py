"""
Pydantic schemas for reports and dashboard metrics.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class DashboardMetricsResponse(BaseModel):
    total_reviews: int
    suspicious_reviews_count: int
    suspicious_reviews_percentage: float
    total_products: int
    total_reviewers: int
    detected_clusters_count: int
    average_trust_score: float
    risk_tier_breakdown: Dict[str, int]
    top_flagged_products: List[Dict[str, Any]]
    recent_suspicious_reviews: List[Dict[str, Any]]


class AuditActionRequest(BaseModel):
    action_type: str  # 'VERIFIED_FLAG', 'DISMISSED_FLAG'
    target_entity: str  # 'REVIEW', 'CLUSTER'
    target_id: int
    notes: Optional[str] = None
