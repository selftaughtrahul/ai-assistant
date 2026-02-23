# Statement of Work (SOW): AI-Powered Customer Support & Demand Management Chatbot

## 1. Project Overview
**Project Name:** AI Customer Support & Demand Management Chatbot
**Client:** Internal (HR/IT/Operations) & E-commerce Divisions
**Date:** 2026-02-23
**Objective:** Develop an intelligent, context-aware chatbot capable of handling customer support queries and internal demand/project tracking using advanced NLP techniques. The bot must be able to interface directly with an internal database to retrieve and update records related to Orders, Demands, Projects, and Resource Availability. It should include a robust mechanism for escalating unclassified or low-confidence queries to a human agent.

## 2. Scope of Work
The project encompasses the design, development, and deployment of a conversational AI agent via a FastAPI backend connected to an SQLite Database.
Key deliverables include:
- **Intelligent NLP Engine:** Implement intent classification leveraging LLMs via external APIs (Groq, Gemini, Hugging Face) or local Transformers.
- **Dynamic Database Operations:** Real-time retrieval and updating of database records including: order status, demand status, project tracking, and resource availability.
- **Context Memory:** Session-aware capabilities allowing the bot to parse conversation history.
- **Human Fallback:** Confidence-score and keyword-based routing to human agents for escalating tickets.
- **API Layer:** Fast and scalable REST APIs using FastAPI, abstracting the LLM orchestration logic.

## 3. Timeline and Milestone
- **Phase 1: Requirements & Initialization:** SOW, BRD, FRD finalization and foundational FastAPI project setup.
- **Phase 2: Database & Router Configuration:** Setup SQLite schemas (Orders, Demands, Projects, Resources) and define basic bot endpoints.
- **Phase 3: NLP Generation & Modularization:** Building the `IntentClassifier` and the class-based scalable `BotReplyGenerator` pipeline.
- **Phase 4: Testing & UAT:** Creating unit testing via `pytest` for db ops, fallback rules, memory, and intent NLP structures.

## 4. Resource Requirements
- AI / NLP Engineer (1)
- Backend Developer (FastAPI/Python) (1)
- Project Manager (1)
- DevOps/Deployment Infrastructure (Cloud VM / Database Hosting)

## 5. Acceptance Criteria
- Chatbot attains successful intent routing and dynamic database retrieval for tracking capabilities.
- Bot can properly *update* database statuses safely via Natural Language queries.
- Fallback triggered successfully when intent confidence drops below threshold (e.g., 0.65) or explicitly requested.
- Unit tests (`pytest`) run natively passing > 90% codebase coverage.
