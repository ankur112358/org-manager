from fastapi import APIRouter, HTTPException
from app.schemas.organization import AdminLogin
from app.utils.auth_utils import authenticate_admin

router = APIRouter()

@router.post("/login")
def admin_login(payload: AdminLogin):
    token = authenticate_admin(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
