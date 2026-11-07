"""
Pydantic schemas for products.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    product_sku: str = Field(..., max_length=100)
    title: str = Field(..., max_length=255)
    category: Optional[str] = "General"
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    average_rating: float
    total_reviews: int
    product_trust_score: float
    created_at: datetime
