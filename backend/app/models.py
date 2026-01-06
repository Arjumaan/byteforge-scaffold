from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    scope: str  # JSON or CSV of domains/paths
    rate_limit_rps: int = 5
    auth_profile: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    jobs: List["Job"] = Relationship(back_populates="target")

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: int = Field(foreign_key="target.id")
    kind: str  # crawl | nuclei | active | report
    status: str = "queued"
    log: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    target: Optional[Target] = Relationship(back_populates="jobs")

class Finding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: int = Field(foreign_key="target.id")
    title: str
    severity: str
    owasp: Optional[str] = None
    cwe: Optional[str] = None
    cvss: Optional[str] = None
    description: Optional[str] = None
    remediation: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Evidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    finding_id: int = Field(foreign_key="finding.id")
    kind: str  # request | response | screenshot | note
    data: str  # store JSON/text; for binaries use object storage in future
    created_at: datetime = Field(default_factory=datetime.utcnow)