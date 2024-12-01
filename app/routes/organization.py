from fastapi import APIRouter, HTTPException
from app.schemas.organization import OrganizationCreate, OrganizationRetrieve
from app.services.db_handler import create_organization, get_organization_by_name

router = APIRouter()

@router.post("/create")
def create_org(payload: OrganizationCreate):
    result = create_organization(payload)
    if not result:
        raise HTTPException(status_code=400, detail="Organization creation failed")
    return {"message": "Organization created successfully"}

@router.get("/get")
def get_org(payload: OrganizationRetrieve):
    org = get_organization_by_name(payload.organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
