from fastapi import APIRouter
from pydantic import BaseModel
from nlp.intent_clf import IntentClassifier
from core.memory import ChatMemory
from core.fallback import FallbackHandler

router = APIRouter()

classifier = IntentClassifier()
memory = ChatMemory()
fallback = FallbackHandler()

class ChatRequest(BaseModel):
    session_id: str
    text: str

class ChatResponse(BaseModel):
    reply: str
    intent: str
    escalated: bool

def generate_bot_reply(intent: str) -> str:
    responses = {
        "Greeting": "Hello! How can I help you today?",
        "Track_Order": "Please provide your order ID to check the status.",
        "Refund": "I can help you with a refund. What is the reason for the return?",
    }
    return responses.get(intent, "I'm sorry, I didn't quite catch that.")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    memory.add_message(request.session_id, "user", request.text)
    
    # 2. NLP Inference (Tokenization & Transformers done inside)
    prediction = classifier.predict(request.text)
    intent = prediction["intent"]
    confidence = prediction["confidence"]
    
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
        
    # 4. Generate Standard AI Response
    reply_text = generate_bot_reply(intent)
    
    # 5. Update Memory (Assistant turn)
    memory.add_message(request.session_id, "assistant", reply_text)
    
    return ChatResponse(
        reply=reply_text,
        intent=intent,
        escalated=False
    )