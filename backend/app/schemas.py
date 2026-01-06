from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

class TargetCreate(BaseModel):
    name: str
    scope: str
    rate_limit_rps: int = 5
    auth_profile: Optional[str] = None

class JobCreate(BaseModel):
    target_id: int
    kind: str

class FindingCreate(BaseModel):
    target_id: int
    title: str
    severity: str
    owasp: Optional[str] = None
    cwe: Optional[str] = None
    cvss: Optional[str] = None
    description: Optional[str] = None
    remediation: Optional[str] = None

class EvidenceCreate(BaseModel):
    finding_id: int
    kind: str
    data: str