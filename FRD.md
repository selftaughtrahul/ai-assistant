# Functional Requirements Document (FRD)

## 1. System Architecture Overview
The system utilizes a modular service architecture hosted via FastAPI and utilizes class-based generation pipelines. It is structured into:
- **API Gateway (`routers/chat.py`):** FastAPI endpoints bridging HTTP requests.
- **NLP Engine (`nlp/intent_clf.py`):** DistilBERT/Transformer configurations for sequence-classification intent extraction.
- **Memory Manager (`core/memory.py`):** Chat history cache handling contextual turn tracking per user session.
- **Agent Handoff Module (`core/fallback.py`):** Confidence & Keyword safety handlers to fall back to human escalation.
- **Database Adapters (`core/db_ops.py`):** SQLite3 bindings safely fetching and updating backend data via parameters.
- **Bot Reply Generator (`core/bot_reply.py`):** Centralized LLM orchestrator (supports Groq, Gemini, and Hugging Face HuggingChat integrations) acting upon predefined intent resolution maps.

## 2. Functional Requirements

### 2.1 Natural Language Processing (NLP)
- **Req 1.1 - Tokenization & Intents:** The system must evaluate token sequences via Hugging Face Transformer pipelines into predefined labels (`Track_Order`, `Track_Demand`, `Project_Status`, `Resource_Availability`, `Update_Order_Status`, `Update_Demand_Status`).
- **Req 1.2 - ID Extraction:** Utilizing Regex matching the engine must extract unique formatting ids (e.g., `ORD-XXXX`, `DEM-XXX`) out of raw string input to search the database.

### 2.2 Database Integrations (Retrievals & Updates)
- **Req 2.1 - Demand Management Entities:** The bot must correctly process lookup tables natively for internal demands, IT project statuses, and resource availabilities without hard crashing.
- **Req 2.2 - Dynamic Table State Commits:** The system must be capable of processing row modifications dynamically (UPDATE TABLE status clauses) for Tracking and Demand workflows.

### 2.3 Context & Session Memory
- **Req 3.1 - Multiturn Memory Injection:** The LLM's system generation prompt must inject the last `N` messages mapped to that specific user's `session_id`.

### 2.4 Human Fallback Mechanism
- **Req 4.1 - Confidence Threshold:** Any queries measuring below `0.65` confidence automatically trigger safe-harbor mode offloading.
- **Req 4.2 - Strict Overrides:** Any message requesting a natural human, agent, or representative bypasses the model immediately.
- **Req 4.3 - Agent Context Transfer:** Safely offload bundled histories to human operator arrays.

### 2.5 API Backend Integration
- **Req 5.1 - Fast API Responses:** The `/chat` Endpoint structure evaluates models dynamically, safely separating LLM generation (`core/bot_reply.py`) from Router code (`routers/chat.py`).
