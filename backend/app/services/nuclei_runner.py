import time
import random

def run_nuclei(job_id: int):
    findings_templates = [
        {"title": "Exposed Git Repository", "severity": "high", "cwe": "CWE-200"},
        {"title": "Outdated Apache Version", "severity": "medium", "cwe": "CWE-937"},
        {"title": "XSS in Search Parameter", "severity": "high", "cwe": "CWE-79"},
        {"title": "Open Redirect", "severity": "low", "cwe": "CWE-601"},
        {"title": "Information Disclosure in Headers", "severity": "info", "cwe": "CWE-200"}
    ]
    time.sleep(8) # Simulate scanning
    
    found = random.sample(findings_templates, k=random.randint(1, 4))
    
    return {
        "job_id": job_id, 
        "status": "completed",
        "findings_count": len(found),
        "matches": found
    }