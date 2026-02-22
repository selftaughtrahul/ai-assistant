import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from nlp.intent_clf import IntentClassifier
from core.config import config

print("ACTIVE PROVIDER CONFIG:", config.ACTIVE_PROVIDER)
print("GROQ API KEY:", "SET" if config.GROQ_API_KEY else "EMPTY")

try:
    print("\n--- Initializing IntentClassifier ---")
    clf = IntentClassifier(model_name="prajjwal1/bert-tiny")
    print("Provider resolved to:", clf.provider)
    print("\n--- Testing Prediction ---")
    result = clf.predict("Where is my order?")
    print("Result:", result)
except Exception as e:
    print(f"Exception caught: {e}")
