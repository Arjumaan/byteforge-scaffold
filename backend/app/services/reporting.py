"""
Report Generator for ByteForge
Generates HTML/JSON security assessment reports
"""
import json
from datetime import datetime
from typing import List, Dict, Any

def run_report(job_id: int, findings: List[Dict] = None, target_name: str = "Target") -> Dict[str, Any]:
    """
    Generate a security assessment report.
    
    Args:
        job_id: The job ID for tracking
        findings: List of findings to include in report
        target_name: Name of the target being reported on
    
    Returns:
        Dictionary with report generation results
    """
    findings = findings or []
    
    # Calculate statistics
    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }
    
    for finding in findings:
        sev = finding.get("severity", "info").lower()
        if sev in severity_counts:
            severity_counts[sev] += 1
    
    # Calculate risk score (0-100)
    risk_score = min(100, (
        severity_counts["critical"] * 25 +
        severity_counts["high"] * 15 +
        severity_counts["medium"] * 8 +
        severity_counts["low"] * 3 +
        severity_counts["info"] * 1
    ))
    
    # Generate HTML report
    html_report = generate_html_report(findings, target_name, severity_counts, risk_score)
    
    # Generate JSON export
    json_export = {
        "report_id": f"BF-{job_id}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now().isoformat(),
        "target": target_name,
        "executive_summary": {
            "total_findings": len(findings),
            "risk_score": risk_score,
            "severity_breakdown": severity_counts
        },
        "findings": findings
    }
    
    return {
        "job_id": job_id,
        "status": "completed",
        "report_id": json_export["report_id"],
        "total_findings": len(findings),
        "risk_score": risk_score,
        "severity_counts": severity_counts,
        "html_available": True,
        "json_export": json_export
    }

def generate_html_report(findings: List[Dict], target_name: str, 
                         severity_counts: Dict, risk_score: int) -> str:
    """Generate HTML report content."""
    
    severity_colors = {
        "critical": "#dc2626",
        "high": "#ea580c",
        "medium": "#ca8a04",
        "low": "#2563eb",
        "info": "#6b7280"
    }
    
    findings_html = ""
    for i, finding in enumerate(findings, 1):
        sev = finding.get("severity", "info").lower()
        color = severity_colors.get(sev, "#6b7280")
        
        findings_html += f"""
        <div class="finding" style="border-left: 4px solid {color}; margin: 16px 0; padding: 16px; background: #f8f9fa;">
            <h3 style="margin: 0 0 8px 0;">
                <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 8px;">
                    {sev.upper()}
                </span>
                {finding.get('title', 'Unknown')}
            </h3>
            <p><strong>CWE:</strong> {finding.get('cwe', 'N/A')}</p>
            <p><strong>Location:</strong> {finding.get('matched_at', 'N/A')}</p>
            <p>{finding.get('description', '')}</p>
        </div>
        """
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ByteForge Security Assessment Report - {target_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #fff; }}
        .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 40px; border-radius: 12px; margin-bottom: 40px; }}
        .header h1 {{ margin: 0; font-size: 2.5rem; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: rgba(255,255,255,0.2); padding: 16px 24px; border-radius: 8px; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; }}
        .stat-label {{ font-size: 0.875rem; opacity: 0.9; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{ color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }}
        .risk-meter {{ height: 20px; background: #e5e7eb; border-radius: 10px; overflow: hidden; }}
        .risk-fill {{ height: 100%; background: linear-gradient(90deg, #22c55e, #eab308, #dc2626); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Security Assessment Report</h1>
        <p>Target: {target_name}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(findings)}</div>
                <div class="stat-label">Total Findings</div>
            </div>
            <div class="stat">
                <div class="stat-value">{severity_counts['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat">
                <div class="stat-value">{severity_counts['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat">
                <div class="stat-value">{risk_score}</div>
                <div class="stat-label">Risk Score</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p>This automated security assessment identified <strong>{len(findings)}</strong> potential security issues.</p>
        <div class="risk-meter">
            <div class="risk-fill" style="width: {risk_score}%;"></div>
        </div>
        <p>Overall Risk Score: <strong>{risk_score}/100</strong></p>
    </div>
    
    <div class="section">
        <h2>Findings</h2>
        {findings_html if findings_html else '<p>No findings to display.</p>'}
    </div>
    
    <footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; text-align: center;">
        <p>Generated by ByteForge Penetration Testing Framework</p>
    </footer>
</body>
</html>
    """
    
    return html