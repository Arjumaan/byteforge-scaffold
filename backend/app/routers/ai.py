from fastapi import APIRouter, Depends
from app.deps import get_current_user
from pydantic import BaseModel
import random

router = APIRouter()

class AIQuery(BaseModel):
    prompt: str

class AIResponse(BaseModel):
    message: str
    suggestions: list[str]
    agent: str = "Antigravity Forge-Agent"

@router.post("/query", response_model=AIResponse)
async def query_ai(body: AIQuery, user=Depends(get_current_user)):
    # Simulated Agent Logic - Combining Antigravity Speed + Claude Reasoning
    responses = [
        "Analysis complete. Based on recent findings, I recommend focusing on the XSS vulnerability in the search parameter. It has the highest exploitability score.",
        "Scanning target scope... I've detected a mismatch in CORS configuration that could lead to data leakage. Shall I queue a specialized active scan?",
        "Combining multi-model insights... The exposed .git directory detected earlier is critical. I've drafted a remediation plan for your review.",
        "Agentic reasoning active: Cross-referencing OWASP Top 10 with current matches. You have 3 Critical and 5 Medium findings. Priority: SQL Injection.",
    ]
    
    suggestions = [
        "Run Nuclei high-severity templates",
        "Generate PDF remediation report",
        "Redact sensitive findings",
        "Update scope to include subdomains"
    ]
    
    return AIResponse(
        message=random.choice(responses),
        suggestions=random.sample(suggestions, k=3)
    )
