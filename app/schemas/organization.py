from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    email: str
    password: str
    organization_name: str

class OrganizationResponse(BaseModel):
    id: int
    organization_name: str
    admin_email: str

class AdminLogin(BaseModel):
    email: str
    password: str
