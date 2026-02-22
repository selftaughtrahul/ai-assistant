FALLBACK_THRESHOLD = 0.65
EXPLICIT_TRIGGERS = ["talk to a human", "customer service", "agent", "real person"]


class FallbackHandler:
    def __init__(self):
        self.fallback_threshold = FALLBACK_THRESHOLD
        self.explicit_triggers = EXPLICIT_TRIGGERS

    def should_fallback(self, user_text: str, intent: str, confidence: float) -> bool:
        if any(trigger in user_text.lower() for trigger in self.explicit_triggers):
            return True
    
        if confidence < self.fallback_threshold:
            return True
        
        if intent == "Human_Agent_Request":
            return True
        
        return False

    def trigger_human_handoff(self, session_id: str, context: list):
        print(f"HANDOFF TRIGGERED for Session: {session_id}")
        print(f"Context passed: {context}")
        return {"status": "escalated", "message": "Connecting you to a human agent..."}