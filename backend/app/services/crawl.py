"""
Web Crawler Integration for ByteForge
Runs projectdiscovery/katana or httpx-toolkit/gospider
"""
import subprocess
import json
import os
import tempfile
from typing import List, Dict, Any
from urllib.parse import urlparse

def run_crawl(job_id: int, target_url: str = None, depth: int = 3, scope: str = None) -> Dict[str, Any]:
    """
    Run web crawler to discover endpoints and assets.
    
    Args:
        job_id: The job ID for tracking
        target_url: Target URL to crawl
        depth: Crawl depth
        scope: Scope definition (domains to include)
    
    Returns:
        Dictionary with crawl results
    """
    # Try katana first, then gospider, then simulate
    result = run_katana(job_id, target_url, depth)
    if result.get("status") == "tool_not_found":
        result = run_gospider(job_id, target_url, depth)
    if result.get("status") == "tool_not_found":
        result = run_crawl_simulated(job_id, target_url)
    
    return result

def run_katana(job_id: int, target_url: str, depth: int = 3) -> Dict[str, Any]:
    """Run Katana crawler from ProjectDiscovery."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            output_file = f.name
        
        # Resolve katana path
        go_bin = os.path.join(os.path.expanduser("~"), "go", "bin")
        katana_path = os.path.join(go_bin, "katana.exe") if os.name == 'nt' else os.path.join(go_bin, "katana")
        if not os.path.exists(katana_path):
            katana_path = "katana"

        cmd = [
            katana_path,
            "-u", target_url,
            "-d", str(depth),
            "-silent",
            "-jc",  # JavaScript crawling
            "-kf", "all",  # Known files
            "-o", output_file,
            "-timeout", "10"
        ]
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        urls = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            os.unlink(output_file)
        
        # Categorize discovered URLs
        categorized = categorize_urls(urls)
        
        return {
            "job_id": job_id,
            "status": "completed",
            "tool": "katana",
            "target": target_url,
            "total_urls": len(urls),
            "endpoints": categorized.get("endpoints", []),
            "js_files": categorized.get("js", []),
            "api_endpoints": categorized.get("api", []),
            "forms": categorized.get("forms", []),
            "parameters": categorized.get("params", [])
        }
        
    except FileNotFoundError:
        return {"status": "tool_not_found", "tool": "katana"}
    except subprocess.TimeoutExpired:
        return {"job_id": job_id, "status": "timeout", "error": "Katana timed out"}
    except Exception as e:
        return {"job_id": job_id, "status": "error", "error": str(e)}

def run_gospider(job_id: int, target_url: str, depth: int = 3) -> Dict[str, Any]:
    """Run GoSpider crawler."""
    try:
        # Resolve gospider path
        go_bin = os.path.join(os.path.expanduser("~"), "go", "bin")
        gospider_path = os.path.join(go_bin, "gospider.exe") if os.name == 'nt' else os.path.join(go_bin, "gospider")
        if not os.path.exists(gospider_path):
            gospider_path = "gospider"

        cmd = [
            gospider_path,
            "-s", target_url,
            "-d", str(depth),
            "--js",
            "-q"  # Quiet mode
        ]
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        urls = []
        for line in process.stdout.split('\n'):
            if line.strip() and 'http' in line:
                # Extract URL from gospider output format
                parts = line.split()
                for part in parts:
                    if part.startswith('http'):
                        urls.append(part)
        
        categorized = categorize_urls(urls)
        
        return {
            "job_id": job_id,
            "status": "completed",
            "tool": "gospider",
            "target": target_url,
            "total_urls": len(urls),
            "endpoints": categorized.get("endpoints", []),
            "js_files": categorized.get("js", []),
            "api_endpoints": categorized.get("api", [])
        }
        
    except FileNotFoundError:
        return {"status": "tool_not_found", "tool": "gospider"}
    except subprocess.TimeoutExpired:
        return {"job_id": job_id, "status": "timeout", "error": "GoSpider timed out"}
    except Exception as e:
        return {"job_id": job_id, "status": "error", "error": str(e)}

def categorize_urls(urls: List[str]) -> Dict[str, List[str]]:
    """Categorize discovered URLs by type."""
    result = {
        "endpoints": [],
        "js": [],
        "api": [],
        "forms": [],
        "params": []
    }
    
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # JavaScript files
        if path.endswith('.js'):
            result["js"].append(url)
        # API endpoints
        elif '/api/' in path or '/v1/' in path or '/v2/' in path or '/graphql' in path:
            result["api"].append(url)
        # Potential forms
        elif any(x in path for x in ['login', 'register', 'signup', 'contact', 'search', 'upload']):
            result["forms"].append(url)
        # URLs with parameters
        elif parsed.query:
            result["params"].append(url)
        else:
            result["endpoints"].append(url)
    
    return result

def run_crawl_simulated(job_id: int, target_url: str) -> Dict[str, Any]:
    """Simulated crawl results when no crawler is installed."""
    import time
    import random
    
    time.sleep(2)
    
    parsed = urlparse(target_url) if target_url else urlparse("https://example.com")
    base = f"{parsed.scheme}://{parsed.netloc}"
    
    endpoints = [
        f"{base}/",
        f"{base}/about",
        f"{base}/contact",
        f"{base}/login",
        f"{base}/dashboard",
        f"{base}/api/users",
        f"{base}/api/v1/products",
    ]
    
    js_files = [
        f"{base}/assets/js/main.js",
        f"{base}/assets/js/app.bundle.js",
    ]
    
    api_endpoints = [
        f"{base}/api/v1/auth",
        f"{base}/api/v1/users",
        f"{base}/graphql",
    ]
    
    params = [
        f"{base}/search?q=test",
        f"{base}/products?id=1",
    ]
    
    return {
        "job_id": job_id,
        "status": "completed",
        "tool": "simulated",
        "target": target_url,
        "total_urls": len(endpoints) + len(js_files) + len(api_endpoints) + len(params),
        "endpoints": random.sample(endpoints, k=min(5, len(endpoints))),
        "js_files": js_files,
        "api_endpoints": api_endpoints,
        "parameters": params,
        "note": "No crawler installed. Install katana: go install github.com/projectdiscovery/katana/cmd/katana@latest"
    }