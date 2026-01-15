"""
Integrations Service
Handles external connections to Jira, Slack, Discord, etc.
"""
import httpx
import json
from typing import Dict, Any, List

class IntegrationService:
    @staticmethod
    async def send_slack_alert(webhook_url: str, message: str, severity: str = "info"):
        """Send a formatted alert to Slack."""
        colors = {
            "critical": "#dc2626",
            "high": "#ea580c",
            "medium": "#eab308",
            "info": "#3b82f6",
            "success": "#22c55e"
        }
        
        payload = {
            "attachments": [
                {
                    "color": colors.get(severity, "#3b82f6"),
                    "text": message,
                    "footer": "ByteForge Security",
                    "footer_icon": "https://byteforge.io/logo.png"
                }
            ]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(webhook_url, json=payload)
            return True
        except Exception as e:
            print(f"Slack Alert Failed: {str(e)}")
            return False

    @staticmethod
    async def create_jira_ticket(
        jira_url: str, 
        auth: tuple, 
        project_key: str, 
        summary: str, 
        description: str,
        priority: str = "Medium"
    ):
        """Create a Jira issue for a finding."""
        # Mapping ByteForge Severity -> Jira Priority
        priority_map = {
            "critical": "Highest",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "info": "Lowest"
        }
        
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Bug"},
                "priority": {"name": priority_map.get(priority.lower(), "Medium")}
            }
        }
        
        try:
            # Placeholder for actual API call
            # async with httpx.AsyncClient(auth=auth) as client:
            #     resp = await client.post(f"{jira_url}/rest/api/2/issue", json=payload)
            #     return resp.json()
            return {"key": "BF-101", "self": f"{jira_url}/browse/BF-101"}
        except Exception as e:
            print(f"Jira Creation Failed: {str(e)}")
            return None

    @staticmethod
    async def send_discord_webhook(webhook_url: str, message: str):
        """Send simple discord message."""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(webhook_url, json={"content": message})
        except:
            pass

integrations = IntegrationService()
