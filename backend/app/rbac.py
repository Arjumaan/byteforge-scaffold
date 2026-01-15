"""
Access Control Logic
"""
from fastapi import HTTPException, status
from app.models import User

def require_role(user: User, required_roles: list[str]):
    """
    Enforce Role-Based Access Control (RBAC).
    Usage: require_role(current_user, ["admin", "superadmin"])
    """
    if user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operation not permitted. Required roles: {required_roles}"
        )
    return True

def is_admin(user: User):
    return require_role(user, ["admin"])
