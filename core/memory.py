from typing import List, Dict, Optional



class ChatMemory:
    def __init__(self):
        self.conversation_store: Dict[str, List[Dict[str, str]]] = {}
        self.limit = 10

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.conversation_store:
            self.conversation_store[session_id] = []
        
        self.conversation_store[session_id].append({"role": role, "content": content})
        
        if len(self.conversation_store[session_id]) > self.limit:
            self.conversation_store[session_id].pop(0)

    def get_history(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        return self.conversation_store.get(session_id, [])[-limit:]

    def clear(self, session_id: str):
        self.conversation_store[session_id] = []

    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        return self.conversation_store.get(session_id, [])