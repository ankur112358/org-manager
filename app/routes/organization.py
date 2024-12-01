from fastapi import APIRouter, HTTPException
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.services.db_handler import create_organization, get_organization_by_name

router = APIRouter()

@router.post("/create", status_code=201)
def create_org(payload: OrganizationCreate):
    org_id = create_organization(payload)
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization creation failed")
    return {"message": "Organization created successfully", "id": org_id}

@router.get("/get/", response_model=OrganizationResponse)
def get_org(organization_name: str):
    org = get_organization_by_name(organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    # TODO: remove the salt and the hashed passwords
    return OrganizationResponse(**org.__dict__)
