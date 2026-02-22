from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

MODEL_NAME = "distilbert-base-uncased"

INTENTS = ["Greeting", "Track_Order", "Refund", "Human_Agent_Request", "Unknown"]





class IntentClassifier:
    def __init__(self, model_name=MODEL_NAME, intents=INTENTS):
        self.intents = intents
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(intents))

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt",truncation=True,padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted_class_idx = torch.max(probs, dim=1)
        intent = self.intents[predicted_class_idx.item()]
        
        return {
            "intent": intent,
            "confidence": confidence.item()
        }
if __name__ == "__main__":
    classifier = IntentClassifier()
    print(classifier.predict("Hello, how are you?"))