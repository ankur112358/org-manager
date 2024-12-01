import logging
from fastapi import FastAPI
from app.routes.organization import router as org_router
from app.routes.auth import router as auth_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("org_manager")
app = FastAPI(title="Organization Management API")

# Include routers
app.include_router(org_router, prefix="/org", tags=["Organization"])
app.include_router(auth_router, prefix="/admin", tags=["Authentication"])
