import os
import sys
from pathlib import Path

# Provide access to core module
sys.path.append(str(Path(__file__).parent.parent))
from core.config import config

INTENTS = ["Greeting", "Track_Order", "Refund", "Human_Agent_Request", "Unknown"]

class IntentClassifier:
    def __init__(self, provider=None, model_name=None, intents=INTENTS):
        self.intents = intents
        
        # Determine the active provider
        # If user explicitly passes a model_name, we assume they want local_transformers
        # This helps maintain backward compatibility with tests
        self.provider = provider or config.ACTIVE_PROVIDER
        if model_name and provider is None:
            self.provider = "groq"
            self.model_name = model_name
        else:
            self.model_name = model_name

        self.model = None
        self.tokenizer = None

        if self.provider == "local_transformers":
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            self.model_name = self.model_name or config.HF_MODEL
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=len(self.intents))
            
        elif self.provider == "huggingface":
            import requests
            self.hf_model = self.model_name or config.HF_MODEL
            self.hf_api_key = config.HF_API_KEY
            self.requests = requests
            
        elif self.provider == "groq":
            from groq import Groq
            # Note: Groq expects an API key. If it's missing, it will raise an error.
            self.groq_client = Groq(api_key=config.GROQ_API_KEY)
            self.groq_model = self.model_name or config.GROQ_MODEL
            
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            model_name_to_use = self.model_name or config.GEMINI_MODEL
            self.gemini_model = genai.GenerativeModel(model_name_to_use)
            
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _create_prompt(self, text):
        return (
            f"You are an intent classification engine. "
            f"Classify the following text into exactly one of these categories: {', '.join(self.intents)}. "
            f"Return ONLY the category name. Do not explain your reasoning. "
            f"Text: '{text}'"
        )
        
    def _parse_llm_response(self, text):
        clean_text = text.strip()
        for intent in self.intents:
            if intent.lower() in clean_text.lower():
                return intent
        return "Unknown"

    def predict(self, text):
        if self.provider == "local_transformers":
            return self._predict_local(text)
        elif self.provider == "huggingface":
            return self._predict_hf_api(text)
        elif self.provider == "groq":
            return self._predict_groq(text)
        elif self.provider == "gemini":
            return self._predict_gemini(text)
            
    def _predict_local(self, text):
        import torch
        import torch.nn.functional as F
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted_class_idx = torch.max(probs, dim=1)
        intent = self.intents[predicted_class_idx.item()]
        
        return {
            "intent": intent,
            "confidence": confidence.item()
        }

    def _predict_hf_api(self, text):
        API_URL = f"https://api-inference.huggingface.co/models/{self.hf_model}"
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        payload = {"inputs": text}
        
        try:
            response = self.requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and isinstance(result[0], list):
                best = max(result[0], key=lambda x: x['score'])
                label = best['label']
                # Try parsing if not matching
                if label not in self.intents:
                    label = self._parse_llm_response(label)
                return {"intent": label, "confidence": best['score']}
            else:
                return {"intent": "Unknown", "confidence": 0.0}
        except Exception as e:
            return {"intent": "Unknown", "confidence": 0.0}

    def _predict_groq(self, text):
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": self._create_prompt(text)}],
                model=self.groq_model,
                temperature=0.0,
                max_tokens=10,
            )
            intent = self._parse_llm_response(chat_completion.choices[0].message.content)
            return {"intent": intent, "confidence": 1.0}
        except Exception as e:
            print(f"[Groq API Error] {e}")
            return {"intent": "Unknown", "confidence": 0.0}

    def _predict_gemini(self, text):
        try:
            response = self.gemini_model.generate_content(
                self._create_prompt(text),
                generation_config=self.gemini_model.GenerationConfig(temperature=0.0)
            )
            intent = self._parse_llm_response(response.text)
            return {"intent": intent, "confidence": 1.0}
        except Exception as e:
            print(f"[Gemini API Error] {e}")
            return {"intent": "Unknown", "confidence": 0.0}

if __name__ == "__main__":
    # Test your Groq fallback logic!
    classifier = IntentClassifier(provider="groq", model_name="llama-3.3-70b-versatile")
    print(f"Testing Model: {classifier.model_name} via {classifier.provider}")
    print("Result:", classifier.predict("Hello, how are you?"))