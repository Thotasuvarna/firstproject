"""
Pydantic schemas for reviews and analysis results.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ReviewAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    duplicate_similarity_score: float
    sentiment_polarity: float
    rating_divergence_score: float
    ml_prediction_prob: float
    composite_suspicion_score: float
    risk_tier: str
    explainability_factors: Optional[Dict[str, Any]] = None
    analyzed_at: datetime


class ReviewCreate(BaseModel):
    product_sku: str
    reviewer_identifier: str = Field(..., description="Email, username, or external ID (will be pseudonymized)")
    rating: float = Field(..., ge=1.0, le=5.0)
    review_title: Optional[str] = ""
    review_text: str = Field(..., min_length=2)
    review_date: Optional[datetime] = None
    is_verified_purchase: Optional[bool] = False


class ReviewBatchUpload(BaseModel):
    reviews: List[ReviewCreate]


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    reviewer_id: int
    rating: float
    review_title: str
    review_text: str
    review_date: datetime
    is_verified_purchase: bool
    created_at: datetime
    analysis: Optional[ReviewAnalysisResponse] = None
