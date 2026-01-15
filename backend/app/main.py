import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings
from app.routers import auth, targets, jobs, findings, evidence, ai
from app.db import init_db

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Global Rate Limiter (Denial of Service protection)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=f"{settings.PROJECT_NAME} Scaffold", version=settings.PROJECT_VERSION)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Security: CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Security: Trusted Host
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
)

# Security: Mandatory Headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Skip strict CSP for API docs (Swagger UI needs external scripts)
    if not request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' http://localhost:8000;"
    
    return response

@app.on_event("startup")
async def on_startup():
    logger.info("Starting up ByteForge Scaffold API...")
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(targets.router, prefix="/targets", tags=["targets"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(findings.router, prefix="/findings", tags=["findings"])
app.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "byteforge-api"}