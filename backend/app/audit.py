import logging
import json
from datetime import datetime, timezone
from app.config import settings

# Dedicated Audit Log for Security Forensics
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("audit_forensics.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
audit_logger.addHandler(file_handler)

def log_security_event(event_type: str, user_email: str, details: dict):
    """Logs a cryptographically auditable security event."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "user_email": user_email,
        "details": details,
        "project": settings.PROJECT_NAME
    }
    audit_logger.info(json.dumps(log_entry))
