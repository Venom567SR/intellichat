from typing import Dict, Any
from ..agents_prompts.intent_prompt import INTENT_PROMPT

class IntentAgent:
    """Classifies the intent of user queries"""

    def __init__(self):
        self.prompt = INTENT_PROMPT
        self.intents = ["billing", "technical", "general", "complaint", "feedback"]

    async def classify(self, query: str) -> Dict[str, Any]:
        # Stub implementation
        return {
            "intent": "general",
            "confidence": 0.85,
            "sub_intents": []
        }

    def validate_intent(self, intent: str) -> bool:
        return intent in self.intents
