from fastapi import APIRouter
from pydantic import BaseModel
from nlp.intent_clf import IntentClassifier
from core.memory import ChatMemory
from core.fallback import FallbackHandler
from core.config import config

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

def generate_bot_reply(intent: str, user_text: str, context_history: list) -> str:
    system_prompt = (
        f"You are a helpful customer support agent. "
        f"The user's query has been classified as the intent: {intent}. "
        f"Answer the user's question politely and concisely based on their intent."
    )
    
    # Format memory for context
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in context_history])
    
    full_prompt = f"{system_prompt}\n\nChat History:\n{history_text}\n\nUser: {user_text}\nAssistant:"

    provider = config.ACTIVE_PROVIDER
    
    try:
        if provider == "groq":
            from groq import Groq
            client = Groq(api_key=config.GROQ_API_KEY)
            # Use a fast LLM for generating responses. 
            # Note: you might eventually want a separate chat model config vs clf config
            model = config.GROQ_MODEL 
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    *context_history,
                    {"role": "user", "content": user_text}
                ],
                model=model,
                temperature=0.7,
                max_tokens=250,
            )
            return response.choices[0].message.content
            
        elif provider == "gemini":
            from google import genai
            client = genai.Client(api_key=config.GEMINI_API_KEY)
            # Gemini models
            model = config.GEMINI_MODEL
            # format as turns
            contents = [f"{msg['role']}: {msg['content']}" for msg in context_history]
            contents.append(f"system: {system_prompt}")
            contents.append(f"user: {user_text}")
            
            response = client.models.generate_content(
                model=model,
                contents="\n".join(contents),
            )
            return response.text
            
        elif provider == "huggingface" or provider == "local_transformers":
            # For HF/Local, simulating an instruction tuned bot via API
            import requests
            API_URL = f"https://api-inference.huggingface.co/models/{config.HF_MODEL}"
            headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
            payload = {
                "inputs": full_prompt,
                "parameters": {"max_new_tokens": 100, "return_full_text": False}
            }
            res = requests.post(API_URL, headers=headers, json=payload)
            res.raise_for_status()
            
            # Hugging Face returns a list of dictionaries.
            result_data = res.json()
            if isinstance(result_data, list) and "generated_text" in result_data[0]:
                 return result_data[0]["generated_text"].strip()
            return str(result_data)
            
    except Exception as e:
        print(f"Reply Generation Error: {e}")
        
    # Ultimate fallback static responses if generation fails.
    responses = {
        "Greeting": "Hello! How can I help you today?",
        "Track_Order": "Please provide your order ID to check the status.",
        "Refund": "I can help you with a refund. What is the reason for the return?",
    }
    return responses.get(intent, "I'm sorry, I didn't quite catch that. How can I help you?")
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
        
    # 4. Generate Standard AI Response using active LLM
    context = memory.get_context(request.session_id)
    reply_text = generate_bot_reply(intent, request.text, context)
    
    # 5. Update Memory (Assistant turn)
    memory.add_message(request.session_id, "assistant", reply_text)
    
    return ChatResponse(
        reply=reply_text,
        intent=intent,
        escalated=False
    )