"""
Job Scheduler Integration
Uses APScheduler to trigger recurring security scans.
"""
import asyncio
from typing import Dict, Any

# Mock APScheduler interface for now to avoid dependency errors if not installed
class JobScheduler:
    def __init__(self):
        self.jobs = {}
        
    def add_scheduled_job(self, job_id: str, cron_expression: str, task_func: Any, args: list):
        """
        Schedule a recurring job.
        cron_expression: "0 2 * * 0" (Every Sunday at 2 AM)
        """
        self.jobs[job_id] = {
            "cron": cron_expression,
            "task": task_func.__name__,
            "args": args,
            "status": "scheduled"
        }
        return {"id": job_id, "status": "scheduled", "next_run": "Sunday 2:00 AM"}

    def remove_job(self, job_id: str):
        if job_id in self.jobs:
            del self.jobs[job_id]
            return True
        return False

scheduler = JobScheduler()

async def schedule_scan(target_id: int, scan_type: str, frequency: str):
    """
    API entry point to schedule a scan.
    frequency: 'daily', 'weekly', 'monthly'
    """
    cron_map = {
        'daily': '0 0 * * *',
        'weekly': '0 0 * * 0',
        'monthly': '0 0 1 * *'
    }
    
    cron = cron_map.get(frequency, '0 0 * * 0')
    job_id = f"target_{target_id}_{scan_type}"
    
    return scheduler.add_scheduled_job(job_id, cron, "run_job", [target_id, scan_type])
