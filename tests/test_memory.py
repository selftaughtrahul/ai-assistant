import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.memory import ChatMemory

def test_chat_memory_initialization():
    memory = ChatMemory()
    assert memory.conversation_store == {}
    assert memory.limit == 10

def test_add_message():
    memory = ChatMemory()
    memory.add_message("session_1", "user", "Hello")
    history = memory.get_context("session_1")
    assert len(history) == 1
    assert history[0] == {"role": "user", "content": "Hello"}

    memory.add_message("session_1", "assistant", "Hi there!")
    history = memory.get_context("session_1")
    assert len(history) == 2
    assert history[1] == {"role": "assistant", "content": "Hi there!"}

def test_memory_limit():
    memory = ChatMemory()
    memory.limit = 3
    for i in range(5):
        memory.add_message("session_limit", "user", f"Message {i}")
    
    # Store keeps length within limits where it trims older messages first
    # So if limit is 3, we should only have messages 2, 3, 4
    history = memory.get_context("session_limit")
    assert len(history) == 3
    assert history[0]["content"] == "Message 2"
    assert history[2]["content"] == "Message 4"

def test_clear_memory():
    memory = ChatMemory()
    memory.add_message("session_clear", "user", "Test")
    memory.clear("session_clear")
    assert memory.get_context("session_clear") == []
