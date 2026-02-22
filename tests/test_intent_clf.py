import pytest
from nlp.intent_clf import IntentClassifier

def test_intent_classifier_initialization():
    # Test initialization with default parameters
    clf = IntentClassifier(provider="local_transformers")
    assert clf.tokenizer is not None
    assert clf.model is not None
    assert clf.intents == ["Greeting", "Track_Order", "Refund", "Human_Agent_Request", "Unknown"]

def test_intent_classifier_custom_model_and_intents():
    # Test initialization dynamically using a different model and custom intents
    custom_model_name = "google/bert_uncased_L-2_H-128_A-2" # very small model for testing purposes
    custom_intents = ["Positive", "Negative", "Neutral"]
    
    clf = IntentClassifier(provider="local_transformers", model_name=custom_model_name, intents=custom_intents)
    assert clf.tokenizer is not None
    assert len(clf.intents) == 3
    assert clf.intents == custom_intents
    assert clf.model.config.num_labels == 3

def test_intent_classifier_prediction_structure():
    # Test that the prediction returns a dictionary with 'intent' and 'confidence'
    clf = IntentClassifier(provider="local_transformers")
    result = clf.predict("Hello, how are you today?")
    
    assert isinstance(result, dict)
    assert "intent" in result
    assert "confidence" in result
    assert isinstance(result["intent"], str)
    assert result["intent"] in clf.intents
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0

def test_intent_classifier_dynamic_prediction():
    # Test prediction step with custom classes/model
    custom_model_name = "google/bert_uncased_L-2_H-128_A-2"
    custom_intents = ["Custom_Intent_A", "Custom_Intent_B", "Custom_Intent_C"]
    
    clf = IntentClassifier(provider="local_transformers", model_name=custom_model_name, intents=custom_intents)
    result = clf.predict("Test sentence here")
    
    assert result["intent"] in custom_intents
    assert 0.0 <= result["confidence"] <= 1.0
