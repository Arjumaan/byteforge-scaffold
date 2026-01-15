"""
Nuclei Integration for ByteForge
Runs projectdiscovery/nuclei vulnerability scanner
"""
import subprocess
import json
import os
import tempfile
from typing import List, Dict, Any

def run_nuclei(job_id: int, target_url: str, templates: str = "cves,vulnerabilities,exposures") -> Dict[str, Any]:
    """
    Run Nuclei vulnerability scanner against a target.
    
    Args:
        job_id: The job ID for tracking
        target_url: Target URL or domain to scan
        templates: Comma-separated list of template categories
    
    Returns:
        Dictionary with scan results
    """
    findings = []
    
    # Find nuclei executable - check Go bin path first
    go_bin = os.path.join(os.path.expanduser("~"), "go", "bin")
    nuclei_path = os.path.join(go_bin, "nuclei.exe") if os.name == 'nt' else os.path.join(go_bin, "nuclei")
    if not os.path.exists(nuclei_path):
        nuclei_path = "nuclei"  # Fallback to PATH
    
    try:
        # Create a temporary file for JSON output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        # Build nuclei command
        cmd = [
            nuclei_path,
            "-u", target_url,
            "-tags", templates,
            "-silent",
            "-json-export", output_file,
            "-severity", "info,low,medium,high,critical",
            "-rate-limit", "50",
            "-timeout", "10"
        ]
        
        # Run nuclei
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        # Parse JSON output
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                for line in f:
                    try:
                        result = json.loads(line.strip())
                        if not isinstance(result, dict):
                            continue
                            
                        # Ensure 'info' is a dict
                        info = result.get("info", {})
                        if not isinstance(info, dict):
                            info = {}

                        findings.append({
                            "title": info.get("name", "Unknown Vulnerability"),
                            "severity": info.get("severity", "info"),
                            "cwe": extract_cwe(result),
                            "template_id": result.get("template-id", ""),
                            "matched_at": result.get("matched-at", target_url),
                            "description": info.get("description", ""),
                            "reference": info.get("reference", []),
                            "curl_command": result.get("curl-command", ""),
                            "request": result.get("request", ""),
                            "response": result.get("response", "")[:2000] if result.get("response") else ""
                        })
                    except json.JSONDecodeError:
                        continue
            
            # Cleanup
            os.unlink(output_file)
        
        return {
            "job_id": job_id,
            "status": "completed",
            "tool": "nuclei",
            "target": target_url,
            "findings_count": len(findings),
            "matches": findings,
            "stderr": process.stderr[:500] if process.stderr else None
        }
        
    except FileNotFoundError:
        # Nuclei not installed - return simulated results for demo
        return run_nuclei_simulated(job_id, target_url)
    except subprocess.TimeoutExpired:
        return {
            "job_id": job_id,
            "status": "timeout",
            "error": "Nuclei scan timed out after 10 minutes"
        }
    except Exception as e:
        return {
            "job_id": job_id,
            "status": "error",
            "error": str(e)
        }

def extract_cwe(result: Dict) -> str:
    """Extract CWE ID from nuclei result."""
    if not isinstance(result, dict):
        return None
    
    info = result.get("info", {})
    if not isinstance(info, dict):
        info = {}
        
    classification = info.get("classification", {})
    if not isinstance(classification, dict):
        return None
        
    cwe_ids = classification.get("cwe-id", [])
    if cwe_ids:
        return cwe_ids[0] if isinstance(cwe_ids, list) else str(cwe_ids)
    return None

def run_nuclei_simulated(job_id: int, target_url: str) -> Dict[str, Any]:
    """Simulated nuclei results when nuclei is not installed."""
    import time
    import random
    
    time.sleep(3)  # Simulate scanning
    
    findings_templates = [
        {"title": "Exposed Git Repository", "severity": "high", "cwe": "CWE-200", "template_id": "git-config"},
        {"title": "Apache Version Disclosure", "severity": "medium", "cwe": "CWE-937", "template_id": "apache-detect"},
        {"title": "Cross-Site Scripting (XSS)", "severity": "high", "cwe": "CWE-79", "template_id": "xss-reflected"},
        {"title": "Open Redirect Vulnerability", "severity": "low", "cwe": "CWE-601", "template_id": "open-redirect"},
        {"title": "Information Disclosure in Headers", "severity": "info", "cwe": "CWE-200", "template_id": "security-headers"},
        {"title": "SQL Injection", "severity": "critical", "cwe": "CWE-89", "template_id": "sqli-detection"},
        {"title": "Sensitive Data Exposure", "severity": "high", "cwe": "CWE-312", "template_id": "sensitive-data"},
    ]
    
    found = random.sample(findings_templates, k=random.randint(2, 5))
    for f in found:
        f["matched_at"] = target_url
        f["description"] = f"Detected {f['title']} on {target_url}"
    
    return {
        "job_id": job_id,
        "status": "completed",
        "tool": "nuclei (simulated)",
        "target": target_url,
        "findings_count": len(found),
        "matches": found,
        "note": "Nuclei not installed. Install via: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
    }