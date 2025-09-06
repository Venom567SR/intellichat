from typing import Dict, Any
from ..agents_prompts.billing_prompt import BILLING_PROMPT

class BillingAgent:
    """Handles billing and payment related queries"""

    def __init__(self):
        self.prompt = BILLING_PROMPT

    async def handle(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Stub implementation
        return {
            "response": "For billing inquiries, please check our pricing page.",
            "action_required": False,
            "billing_info": {
                "plans": ["Basic", "Pro", "Enterprise"],
                "current_plan": context.get("user_plan", "Basic") if context else "Basic"
            }
        }

    def validate_billing_action(self, action: str) -> bool:
        allowed_actions = ["view_invoice", "update_payment", "change_plan", "cancel"]
        return action in allowed_actions
