from typing import Dict, Any, List
from ..agents_prompts.technical_prompt import TECHNICAL_PROMPT

class TechnicalAgent:
    """Handles technical support and troubleshooting"""

    def __init__(self):
        self.prompt = TECHNICAL_PROMPT
        self.common_issues = [
            "login_problems",
            "performance_issues",
            "integration_errors",
            "api_issues"
        ]

    async def handle(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Stub implementation
        return {
            "response": "I can help with technical issues. Please describe the problem.",
            "troubleshooting_steps": [],
            "requires_ticket": False
        }

    def diagnose_issue(self, symptoms: List[str]) -> str:
        return "general_technical_issue"
