from typing import Dict, Any, List
from ..agents_prompts.response_generator_prompt import RESPONSE_GENERATOR_PROMPT

class ResponseGeneratorAgent:
    """Generates and formats the final response"""

    def __init__(self):
        self.prompt = RESPONSE_GENERATOR_PROMPT

    async def generate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Stub implementation
        response = self.format_response(
            query=context.get("query", ""),
            intent=context.get("intent", "general"),
            retrieved_docs=context.get("retrieved_docs", []),
            sentiment=context.get("sentiment", "neutral")
        )

        return {
            "response": response,
            "metadata": {
                "confidence": 0.9,
                "sources_used": len(context.get("retrieved_docs", [])),
                "response_type": "generated"
            }
        }

    def format_response(self, query: str, intent: str, retrieved_docs: List[str],
                       sentiment: str) -> str:
        base_response = "Thank you for your query. "

        if intent == "billing":
            base_response += "For billing inquiries, "
        elif intent == "technical":
            base_response += "For technical support, "

        base_response += "I'm here to help you."

        if retrieved_docs:
            base_response += f" I found {len(retrieved_docs)} relevant documents."

        return base_response

    def add_followup_questions(self, response: str, context: Dict[str, Any]) -> str:
        followups = [
            "Is there anything else I can help you with?",
            "Would you like more information?",
            "Can I assist you with anything else?"
        ]
        return f"{response}\n\n{followups[0]}"
