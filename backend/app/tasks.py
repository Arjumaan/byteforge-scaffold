import asyncio
from app.services.nuclei_runner import run_nuclei
from app.services.crawl import run_crawl
from app.services.active_scan import run_active
from app.services.reporting import run_report
from app.db import async_session
from app.models import Job, Finding
import json

async def _run_job_async(job_id: int, kind: str):
    async with async_session() as session:
        job = await session.get(Job, job_id)
        if not job:
            return
        
        job.status = "running"
        await session.commit()
        
        try:
            result = {}
            if kind == "crawl":
                result = run_crawl(job_id)
            elif kind == "nuclei":
                result = run_nuclei(job_id)
                # Simulated: Create actual findings in DB
                if "matches" in result:
                    for match in result["matches"]:
                        finding = Finding(
                            target_id=job.target_id,
                            title=match["title"],
                            severity=match["severity"],
                            cwe=match.get("cwe"),
                            description=f"Nuclei found {match['title']}"
                        )
                        session.add(finding)
            elif kind == "active":
                result = run_active(job_id)
            elif kind == "report":
                result = run_report(job_id)
            
            job.status = "completed"
            job.log = json.dumps(result)
        except Exception as e:
            job.status = "failed"
            job.log = str(e)
            
        await session.commit()

def run_job(job_id: int, kind: str):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        asyncio.create_task(_run_job_async(job_id, kind))
    else:
        loop.run_until_complete(_run_job_async(job_id, kind))
