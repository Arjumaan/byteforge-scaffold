import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.routers import auth, targets, jobs, findings, evidence
from app.db import init_db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ByteForge Scaffold - Pentest Framework", version="0.1.0")

# Security: CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Security: Trusted Host
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=os.getenv("ALLOWED_HOSTS", "*").split(",")
)

@app.on_event("startup")
async def on_startup():
    logger.info("Starting up ByteForge Scaffold API...")
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(targets.router, prefix="/targets", tags=["targets"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(findings.router, prefix="/findings", tags=["findings"])
app.include_router(evidence.router, prefix="/evidence", tags=["evidence"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "byteforge-api"}