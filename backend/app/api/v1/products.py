"""
Product Management Endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve catalog products with optional search and category filters."""
    query = db.query(Product)
    if search:
        query = query.filter(
            Product.title.ilike(f"%{search}%") | Product.product_sku.ilike(f"%{search}%")
        )
    if category:
        query = query.filter(Product.category == category)
        
    return query.order_by(Product.id.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Creates a new product SKU in the catalog."""
    existing = db.query(Product).filter(Product.product_sku == product_in.product_sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product_in.product_sku}' already exists."
        )
    
    product = Product(
        product_sku=product_in.product_sku,
        title=product_in.title,
        category=product_in.category or "General",
        description=product_in.description,
        average_rating=0.0,
        total_reviews=0,
        product_trust_score=100.0
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve details for a single product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
