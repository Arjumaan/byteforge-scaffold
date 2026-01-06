import time
import random

def run_crawl(job_id: int):
    # Simulated crawling process
    urls_found = [
        "/", "/login", "/admin", "/api/v1/users", "/static/js/main.js", 
        "/config.php", "/.git/config", "/wp-login.php"
    ]
    time.sleep(5)  # Simulate network latency
    
    return {
        "job_id": job_id, 
        "status": "completed",
        "urls_discovered": random.sample(urls_found, k=random.randint(3, 8)),
        "params_found": ["id", "user", "debug", "admin"]
    }