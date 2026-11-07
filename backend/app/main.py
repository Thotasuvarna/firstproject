"""
FastAPI Main Application Entrypoint.
Initializes database tables, configures CORS, and registers API V1 endpoints.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, ACTIVE_DB_DIALECT
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup & shutdown events."""
    logger.info("[Startup] Initializing database tables...")
    init_db()
    logger.info(f"[Startup] Application online with active database dialect: {ACTIVE_DB_DIALECT}")
    yield
    logger.info("[Shutdown] Application terminating cleanly.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade AI system to detect fraudulent product reviews and coordinated reviewer networks using NLP, ML, and Graph Theory.",
    lifespan=lifespan
)

# CORS Middleware configuration
# In development, allow all origins so the Vite dev-server proxy and
# direct browser requests both work without CORS errors.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Open for development — restrict in production
    allow_credentials=False,       # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
def root_status():
    """System status and API overview."""
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database_dialect": ACTIVE_DB_DIALECT,
        "docs_url": "/docs",
        "api_v1_prefix": settings.API_V1_STR
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "database": ACTIVE_DB_DIALECT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
