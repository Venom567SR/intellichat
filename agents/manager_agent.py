from typing import Dict, Any
import yaml
from ..agents_prompts.manager_prompt import MANAGER_PROMPT

class ManagerAgent:
    """Orchestrates the flow between different agents"""

    def __init__(self):
        self.prompt = MANAGER_PROMPT
        self.config = self._load_config()
        self.state = {}

    def _load_config(self):
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    async def run(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Initialize state
        self.state = {
            "query": query,
            "context": context or {},
            "intent": None,
            "sentiment": None,
            "retrieved_docs": [],
            "response": None
        }
        # Pipeline stub - call other agents (not implemented here)
        return {
            "response": "This is a stub response from the Manager Agent.",
            "metadata": self.state
        }

    def get_next_agent(self, current_state: Dict[str, Any]) -> str:
        return "intent_agent"
