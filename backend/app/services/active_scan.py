"""
Active Scanner Module for ByteForge
Custom active security testing modules
"""
import subprocess
import json
import re
import time
import random
from typing import List, Dict, Any
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import httpx

def run_active(job_id: int, target_url: str = None, endpoints: List[str] = None) -> Dict[str, Any]:
    """
    Run active security scans against target.
    
    Args:
        job_id: The job ID for tracking
        target_url: Base target URL
        endpoints: List of endpoints to test (from crawl results)
    
    Returns:
        Dictionary with active scan results
    """
    findings = []
    scan_modules = [
        ("XSS Detection", scan_xss),
        ("SQL Injection Detection", scan_sqli),
        ("Path Traversal Detection", scan_path_traversal),
        ("SSRF Detection", scan_ssrf),
        ("Open Redirect Detection", scan_open_redirect),
        ("Header Injection Detection", scan_header_injection),
    ]
    
    test_endpoints = endpoints or [target_url] if target_url else []
    
    for module_name, scanner_func in scan_modules:
        try:
            module_findings = scanner_func(test_endpoints[:10])  # Limit to 10 endpoints
            findings.extend(module_findings)
        except Exception as e:
            continue
    
    return {
        "job_id": job_id,
        "status": "completed",
        "tool": "active_scanner",
        "target": target_url,
        "modules_executed": len(scan_modules),
        "endpoints_tested": len(test_endpoints[:10]),
        "findings_count": len(findings),
        "matches": findings
    }

def scan_xss(endpoints: List[str]) -> List[Dict]:
    """Test for Cross-Site Scripting vulnerabilities."""
    findings = []
    xss_payloads = [
        '<script>alert(1)</script>',
        '"><img src=x onerror=alert(1)>',
        "'-alert(1)-'",
        '<svg onload=alert(1)>',
    ]
    
    for url in endpoints:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            continue
            
        for param_name in params:
            for payload in xss_payloads[:2]:  # Test first 2 payloads
                try:
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    test_url = urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, urlencode(test_params, doseq=True), parsed.fragment
                    ))
                    
                    response = httpx.get(test_url, timeout=5, follow_redirects=True)
                    
                    # Check if payload is reflected unencoded
                    if payload in response.text:
                        findings.append({
                            "title": "Reflected XSS Vulnerability",
                            "severity": "high",
                            "cwe": "CWE-79",
                            "parameter": param_name,
                            "payload": payload,
                            "matched_at": url,
                            "evidence": f"Payload reflected in response at {url}",
                            "request": f"GET {test_url}",
                            "response_snippet": response.text[:500]
                        })
                        break  # One finding per parameter is enough
                except:
                    continue
    
    return findings

def scan_sqli(endpoints: List[str]) -> List[Dict]:
    """Test for SQL Injection vulnerabilities."""
    findings = []
    sqli_payloads = [
        "' OR '1'='1",
        "1' AND '1'='1",
        "1; DROP TABLE users--",
        "' UNION SELECT NULL--",
    ]
    
    error_patterns = [
        r"SQL syntax",
        r"mysql_fetch",
        r"ORA-\d{5}",
        r"PostgreSQL.*ERROR",
        r"SQLite3::SQLException",
        r"ODBC SQL Server Driver",
        r"unclosed quotation mark",
    ]
    
    for url in endpoints:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            continue
        
        for param_name in params:
            for payload in sqli_payloads[:2]:
                try:
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    test_url = urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, urlencode(test_params, doseq=True), parsed.fragment
                    ))
                    
                    response = httpx.get(test_url, timeout=5, follow_redirects=True)
                    
                    # Check for SQL error patterns
                    for pattern in error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            findings.append({
                                "title": "SQL Injection Vulnerability",
                                "severity": "critical",
                                "cwe": "CWE-89",
                                "parameter": param_name,
                                "payload": payload,
                                "matched_at": url,
                                "evidence": f"SQL error triggered: {pattern}",
                                "request": f"GET {test_url}"
                            })
                            break
                except:
                    continue
    
    return findings

def scan_path_traversal(endpoints: List[str]) -> List[Dict]:
    """Test for Path Traversal vulnerabilities."""
    findings = []
    traversal_payloads = [
        "../../../etc/passwd",
        "....//....//....//etc/passwd",
        "..\\..\\..\\windows\\win.ini",
    ]
    
    success_patterns = [
        r"root:.*:0:0:",
        r"\[extensions\]",
        r"\[fonts\]",
    ]
    
    for url in endpoints:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Look for file-related parameters
        file_params = [p for p in params if any(x in p.lower() for x in ['file', 'path', 'doc', 'page', 'include'])]
        
        for param_name in file_params:
            for payload in traversal_payloads:
                try:
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    test_url = urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, urlencode(test_params, doseq=True), parsed.fragment
                    ))
                    
                    response = httpx.get(test_url, timeout=5, follow_redirects=True)
                    
                    for pattern in success_patterns:
                        if re.search(pattern, response.text):
                            findings.append({
                                "title": "Path Traversal Vulnerability",
                                "severity": "critical",
                                "cwe": "CWE-22",
                                "parameter": param_name,
                                "payload": payload,
                                "matched_at": url,
                                "evidence": "Sensitive file content detected",
                                "request": f"GET {test_url}"
                            })
                            break
                except:
                    continue
    
    return findings

def scan_ssrf(endpoints: List[str]) -> List[Dict]:
    """Test for Server-Side Request Forgery vulnerabilities."""
    # Placeholder - would need callback server in real implementation
    return []

def scan_open_redirect(endpoints: List[str]) -> List[Dict]:
    """Test for Open Redirect vulnerabilities."""
    findings = []
    redirect_payloads = [
        "https://evil.com",
        "//evil.com",
        "/\\evil.com",
    ]
    
    for url in endpoints:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Look for redirect-related parameters
        redirect_params = [p for p in params if any(x in p.lower() for x in ['url', 'redirect', 'next', 'return', 'goto', 'dest'])]
        
        for param_name in redirect_params:
            for payload in redirect_payloads:
                try:
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    test_url = urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, urlencode(test_params, doseq=True), parsed.fragment
                    ))
                    
                    response = httpx.get(test_url, timeout=5, follow_redirects=False)
                    
                    location = response.headers.get('location', '')
                    if 'evil.com' in location:
                        findings.append({
                            "title": "Open Redirect Vulnerability",
                            "severity": "medium",
                            "cwe": "CWE-601",
                            "parameter": param_name,
                            "payload": payload,
                            "matched_at": url,
                            "evidence": f"Redirects to: {location}",
                            "request": f"GET {test_url}"
                        })
                        break
                except:
                    continue
    
    return findings

def scan_header_injection(endpoints: List[str]) -> List[Dict]:
    """Test for HTTP Header Injection vulnerabilities."""
    # Placeholder
    return []