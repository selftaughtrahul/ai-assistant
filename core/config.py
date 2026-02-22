import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Model Provider Settings: "huggingface", "groq", or "gemini"
    ACTIVE_PROVIDER = os.getenv("ACTIVE_PROVIDER", "huggingface")

    # Hugging Face Settings (Inference API or Local)
    # To use local, leave HF_API_KEY empty and set ACTIVE_PROVIDER="local_transformers"
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-1B-Instruct") # For zero-shot or fine-tuned classification via API

    # Groq Settings
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Gemini Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

config = Config()
