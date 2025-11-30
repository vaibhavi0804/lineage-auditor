"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.config import settings
from app.routers import datasets, profiles, issues, lineage
from app.database import init_db

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])
app.include_router(lineage.router, prefix="/api/lineage", tags=["lineage"])

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs", status_code=302)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": settings.API_VERSION}


logger.info(f"Lineage Auditor API initialized (v{settings.API_VERSION})")
