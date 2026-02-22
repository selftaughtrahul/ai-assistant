# Functional Requirements Document (FRD)

## 1. System Architecture Overview
The system relies on a Microservice-like architecture using FastAPI. It consists of:
- **API Gateway/Interface:** FastAPI endpoints handling incoming user messages.
- **NLP Engine module:** HuggingFace Transformers for intent classification and entity extraction.
- **Memory Manager module:** A fast cache (e.g., Redis or in-memory dict for MVP) to store session context.
- **Agent Handoff module:** Logic to trigger escalations.

## 2. Functional Requirements

### 2.1 Natural Language Processing (NLP)
- **Req 1.1 - Tokenization:** The system must tokenize incoming text applying standard tokenizers (e.g., AutoTokenizer from HuggingFace).
- **Req 1.2 - Intent Classification:** The system must classify the user's intent into pre-defined categories (e.g., 'Track_Order', 'Refund_Request', 'Greeting').
- **Req 1.3 - Confidence Scoring:** The model must output a confidence score for its prediction.

### 2.2 Context Memory
- **Req 2.1 - Session Tracking:** Each user chat must be assigned a unique `session_id`.
- **Req 2.2 - Multi-turn Awareness:** The system must retrieve the last N turns of conversation to provide context to the LLM/Intent classifier.
- **Req 2.3 - Session Expiry:** Context should expire after X minutes of inactivity.

### 2.3 Human Fallback Mechanism
- **Req 3.1 - Confidence Threshold:** If the intent classification confidence is below 0.60, trigger fallback.
- **Req 3.2 - Explicit Escalation:** If the user explicitly asks for "human", "agent", or "support", trigger fallback immediately.
- **Req 3.3 - Handoff Data:** Upon fallback, the system must bundle the `session_id` and the context memory, passing it to the human agent dashboard.

### 2.4 FastAPI Backend Integration
- **Req 4.1 - Chat Endpoint:** Provide a `POST /chat` endpoint taking `{"session_id": string, "text": string}`.
- **Req 4.2 - Non-blocking IO:** Ensure NLP inference does not excessively block the event loop (use ThreadPools if necessary).
