"""
API Router V1.
Consolidates authentication, products, reviews, graph, dashboard, and reports routes.
"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.products import router as products_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.graph import router as graph_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(products_router)
api_router.include_router(reviews_router)
api_router.include_router(graph_router)
api_router.include_router(dashboard_router)
api_router.include_router(reports_router)
