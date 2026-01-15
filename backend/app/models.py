from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship

from app.security import encrypt_data, decrypt_data

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # Encrypted in DB
    scope: str # Encrypted in DB
    rate_limit_rps: int = 5
    auth_profile: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # jobs: List["Job"] = Relationship(back_populates="target")

    def encrypt_fields(self):
        self.name = encrypt_data(self.name)
        self.scope = encrypt_data(self.scope)

    def decrypt_fields(self):
        self.name = decrypt_data(self.name)
        self.scope = decrypt_data(self.scope)

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: int = Field(foreign_key="target.id")
    kind: str  # crawl | nuclei | active | report
    status: str = "queued"
    log: Optional[str] = None # Encrypted in DB
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # target: Optional[Target] = Relationship(back_populates="jobs")

    def encrypt_fields(self):
        if self.log: self.log = encrypt_data(self.log)

    def decrypt_fields(self):
        if self.log: self.log = decrypt_data(self.log)

class Finding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: int = Field(foreign_key="target.id")
    title: str # Encrypted in DB
    severity: str 
    owasp: Optional[str] = None
    cwe: Optional[str] = None
    cvss: Optional[str] = None
    description: Optional[str] = None # Encrypted in DB
    remediation: Optional[str] = None # Encrypted in DB
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def encrypt_fields(self):
        self.title = encrypt_data(self.title)
        if self.description: self.description = encrypt_data(self.description)
        if self.remediation: self.remediation = encrypt_data(self.remediation)

    def decrypt_fields(self):
        self.title = decrypt_data(self.title)
        if self.description: self.description = decrypt_data(self.description)
        if self.remediation: self.remediation = decrypt_data(self.remediation)

class Evidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    finding_id: int = Field(foreign_key="finding.id")
    kind: str  # request | response | screenshot | note
    data: str  # Encrypted in DB
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def encrypt_fields(self):
        self.data = encrypt_data(self.data)

    def decrypt_fields(self):
        self.data = decrypt_data(self.data)