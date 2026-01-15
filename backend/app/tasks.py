"""
Task Runner for ByteForge
Executes security scanning jobs asynchronously
"""
import asyncio
import json
from app.services.nuclei_runner import run_nuclei, run_nuclei_simulated
from app.services.crawl import run_crawl
from app.services.recon import run_subdomain_enum
from app.services.active_scan import run_active
from app.services.reporting import run_report
from app.db import async_session
from app.models import Job, Finding, Target, Evidence
from app.audit import log_security_event

async def _run_job_async(job_id: int, kind: str):
    async with async_session() as session:
        job = await session.get(Job, job_id)
        if not job:
            return
        
        # Get target information
        target = await session.get(Target, job.target_id)
        if target:
            target.decrypt_fields()
        
        target_url = target.scope if target else "https://example.com"
        
        job.status = "running"
        await session.commit()
        
        try:
            result = {}
            
            if kind == "crawl":
                result = run_crawl(job_id, target_url)
                # Store crawled endpoints for later use
                
            elif kind == "recon":
                result = run_subdomain_enum(job_id, target_url)
                
            elif kind == "nuclei":
                result = run_nuclei(job_id, target_url)
                await _store_nuclei_findings(session, job.target_id, result)
                            
            elif kind == "active":
                # Get endpoints from previous crawl if available
                endpoints = [target_url]  # Base case
                
                result = run_active(job_id, target_url, endpoints)
                
                # Create findings from active scan
                if "matches" in result:
                    for match in result["matches"]:
                        finding = Finding(
                            target_id=job.target_id,
                            title=match.get("title", "Active Scan Finding"),
                            severity=match.get("severity", "medium"),
                            cwe=match.get("cwe"),
                            description=f"Active scan detected: {match.get('evidence', '')}",
                            remediation=f"Parameter: {match.get('parameter', 'N/A')}"
                        )
                        finding.encrypt_fields()
                        session.add(finding)
                        await session.flush()
                        
                        # Store request as evidence
                        if match.get("request"):
                            evidence = Evidence(
                                finding_id=finding.id,
                                kind="request",
                                data=f"Payload: {match.get('payload', '')}\n{match.get('request', '')}"
                            )
                            evidence.encrypt_fields()
                            session.add(evidence)
            
            elif kind == "full_scan":
                # 1. Recon
                recon_res = run_subdomain_enum(job_id, target_url)
                
                # 2. Crawl
                crawl_res = run_crawl(job_id, target_url)
                
                # 3. Nuclei
                nuclei_res = run_nuclei(job_id, target_url)
                await _store_nuclei_findings(session, job.target_id, nuclei_res)
                
                result = {
                    "recon": recon_res,
                    "crawl": crawl_res,
                    "nuclei": nuclei_res,
                    "summary": f"Full scan completed. Found {nuclei_res.get('findings_count', 0)} vulnerabilities and {recon_res.get('found_count', 0)} subdomains.",
                    "findings_count": nuclei_res.get("findings_count", 0)
                }

            elif kind == "report":
                result = run_report(job_id)
            
            job.status = "completed"
            job.log = json.dumps(result, default=str)
            job.encrypt_fields()
            
            log_security_event("JOB_COMPLETED", "system_worker", {
                "job_id": job_id, 
                "kind": kind, 
                "status": "success",
                "findings_count": result.get("findings_count", 0)
            })
            
        except Exception as e:
            job.status = "failed"
            job.log = str(e)
            job.encrypt_fields()
            log_security_event("JOB_FAILED", "system_worker", {
                "job_id": job_id, 
                "kind": kind, 
                "error": str(e)
            })
            
        await session.commit()

async def _store_nuclei_findings(session, target_id, result):
    if "matches" in result:
        for match in result["matches"]:
            finding = Finding(
                target_id=target_id,
                title=match.get("title", "Unknown Vulnerability"),
                severity=match.get("severity", "info"),
                cwe=match.get("cwe"),
                description=match.get("description") or f"Detected via {result.get('tool', 'nuclei')} scan.",
                remediation=f"Review the vulnerability at {match.get('matched_at', 'target')}"
            )
            finding.encrypt_fields()
            session.add(finding)
            await session.flush()
            
            # Create evidence for the finding
            if match.get("request") or match.get("curl_command"):
                evidence = Evidence(
                    finding_id=finding.id,
                    kind="request",
                    data=match.get("curl_command") or match.get("request", "")
                )
                evidence.encrypt_fields()
                session.add(evidence)
            
            if match.get("response"):
                evidence = Evidence(
                    finding_id=finding.id,
                    kind="response",
                    data=match.get("response", "")[:2000]
                )
                evidence.encrypt_fields()
                session.add(evidence)

def run_job(job_id: int, kind: str):
    """Entry point for job execution."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        asyncio.create_task(_run_job_async(job_id, kind))
    else:
        loop.run_until_complete(_run_job_async(job_id, kind))
