from fastapi import APIRouter
from pydantic import BaseModel
from nlp.intent_clf import IntentClassifier
from core.memory import ChatMemory
from core.fallback import FallbackHandler
from core.bot_reply import BotReplyGenerator
import sqlite3
import re

router = APIRouter()

classifier = IntentClassifier()
memory = ChatMemory()
fallback = FallbackHandler()
bot_reply_gen = BotReplyGenerator()

class ChatRequest(BaseModel):
    session_id: str
    text: str

class ChatResponse(BaseModel):
    reply: str
    intent: str
    escalated: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    memory.add_message(request.session_id, "user", request.text)
    
    # 2. NLP Inference (Tokenization & Transformers done inside)
    prediction = classifier.predict(request.text)
    intent = prediction["intent"]
    confidence = prediction["confidence"]
    
    print(f"[DEBUG] Intent: {intent}, Confidence: {confidence}")
    
    # 3. Check for Fallback
    if fallback.should_fallback(request.text, intent, confidence):
        context = memory.get_context(request.session_id)
        handoff_res = fallback.trigger_human_handoff(request.session_id, context)
        
        # Bot system relies escalation state back
        memory.add_message(request.session_id, "assistant", handoff_res["message"])
        return ChatResponse(
            reply=handoff_res["message"],
            intent=intent,
            escalated=True
        )
    # 4. Generate Standard AI Response using active LLM
    context = memory.get_context(request.session_id)
    reply_text = bot_reply_gen.generate_reply(intent, request.text, context)
    
    # 5. Update Memory (Assistant turn)
    memory.add_message(request.session_id, "assistant", reply_text)
    
    return ChatResponse(
        reply=reply_text,
        intent=intent,
        escalated=False
    )