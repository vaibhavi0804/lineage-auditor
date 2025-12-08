from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.config import get_settings
from app.routers import datasets, profiles, issues, lineage
from app.database import init_db  # just import, don't call here

settings = get_settings()

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# CORS, routers, etc. (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])
app.include_router(lineage.router, prefix="/api/lineage", tags=["lineage"])


@app.on_event("startup")
def on_startup() -> None:
    # This is where DB tables get created
    init_db()
    logger.info("Database initialized")


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs", status_code=302)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.API_VERSION}


logger.info(f"Lineage Auditor API initialized (v{settings.API_VERSION})")
