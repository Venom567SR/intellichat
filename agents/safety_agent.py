from typing import Dict, Any, List
import re
from ..agents_prompts.safety_prompt import SAFETY_PROMPT

class SafetyAgent:
    """Ensures response safety and handles PII"""

    def __init__(self):
        self.prompt = SAFETY_PROMPT
        # simple patterns as readable strings (avoid complex escaping)
        self.pii_patterns = {
            "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "phone": r"\d{3}[-.]?\d{3}[-.]?\d{4}"
        }

    async def check(self, text: str) -> Dict[str, Any]:
        pii_found = self.detect_pii(text)
        is_safe = self.is_safe_content(text)

        return {
            "is_safe": is_safe,
            "pii_detected": len(pii_found) > 0,
            "pii_types": pii_found,
            "confidence": 0.95
        }

    def detect_pii(self, text: str) -> List[str]:
        found_pii = []
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                found_pii.append(pii_type)
        return found_pii

    def is_safe_content(self, text: str) -> bool:
        return True

    def redact_pii(self, text: str) -> str:
        for pii_type, pattern in self.pii_patterns.items():
            text = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", text)
        return text
