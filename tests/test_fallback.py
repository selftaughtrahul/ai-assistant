import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.fallback import FallbackHandler

def test_fallback_initialization():
    handler = FallbackHandler()
    assert handler.fallback_threshold == 0.65
    assert len(handler.explicit_triggers) > 0

def test_explicit_triggers():
    handler = FallbackHandler()
    
    # Text with explicit trigger
    user_text = "I want to talk to a human agent, please."
    result = handler.should_fallback(user_text, "Unknown", 0.9)
    assert result == True
    
    # Normal text without explicit trigger
    user_text_normal = "What is the status of my order?"
    result_normal = handler.should_fallback(user_text_normal, "Track_Order", 0.9)
    assert result_normal == False

def test_confidence_threshold():
    handler = FallbackHandler()
    
    # High confidence => Not fallback
    res_high = handler.should_fallback("hello", "Greeting", 0.8)
    assert res_high == False
    
    # Low confidence => Fallback
    res_low = handler.should_fallback("something obscure", "Unknown", 0.4)
    assert res_low == True

def test_human_agent_intent():
    handler = FallbackHandler()
    
    res = handler.should_fallback("agent please", "Human_Agent_Request", 0.9)
    assert res == True

def test_trigger_handoff():
    handler = FallbackHandler()
    res = handler.trigger_human_handoff("session_123", [{"role": "user", "content": "help"}])
    
    assert res["status"] == "escalated"
    assert "Connecting you to a human agent" in res["message"]
