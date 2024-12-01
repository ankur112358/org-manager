import logging
from fastapi import APIRouter, HTTPException
from app.schemas.organization import AdminLogin
from app.utils.auth_utils import authenticate_admin
from app.services.db_handler import get_organization_by_email

logger = logging.getLogger("org_manager")
router = APIRouter()

@router.post("/login")
def admin_login(payload: AdminLogin):
    # NOTE: If we have to get the auth of all user not just the admin user, then
    # we can have additional organization data in the payload which can then be
    # used to get the hash and salt from the correct database.
    org = get_organization_by_email(payload.email)
    if not org:
        logger.info(f"Invalid user: {payload.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    salt = org.salt
    hashed_password = org.hashed_password
    token = authenticate_admin(
        email=payload.email,
        password=payload.password,
        salt=salt,
        correct_hashed_password=hashed_password
    )
    if not token:
        logger.info(f"Unauthenticated user: {payload.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
