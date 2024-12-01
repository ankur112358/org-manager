from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    email: str
    password: str
    organization_name: str

class OrganizationRetrieve(BaseModel):
    organization_name: str

class AdminLogin(BaseModel):
    email: str
    password: str
