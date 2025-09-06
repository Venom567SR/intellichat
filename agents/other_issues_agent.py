from typing import Dict, Any
from ..agents_prompts.other_issues_prompt import OTHER_ISSUES_PROMPT

class OtherIssuesAgent:
    """Handles queries that don't fit other categories"""

    def __init__(self):
        self.prompt = OTHER_ISSUES_PROMPT

    async def handle(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Stub implementation
        return {
            "response": "I'll help you with your query. Let me find the right information.",
            "category": "general",
            "confidence": 0.7
        }

    def route_to_human(self, query: str) -> bool:
        return False
