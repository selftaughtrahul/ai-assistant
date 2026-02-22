# AI-Powered Customer Support Chatbot

A simple, fast, and intelligent customer support chatbot built using Python, FastAPI, and Hugging Face Transformers.

This repository is currently under active development. The initial phase involves building a robust Natural Language Processing (NLP) pipeline for intent classification and entity extraction, coupled with a session-aware conversational memory system and fallback mechanism for human agents.

## 🚀 Technologies Used
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - High performance API framework.
*   **NLP & ML:** [Hugging Face Transformers](https://huggingface.co/), [PyTorch](https://pytorch.org/), [Scikit-Learn](https://scikit-learn.org/).
*   **Dependencies:** `uvicorn`, `pydantic`.

## 📁 Project Structure

```
chatbot/
├── core/                   # Shared logic (memory management, agent fallback logic)
├── nlp/                    # NLP Pipeline (tokenizers, intent classification models)
├── routers/                # FastAPI routing and API endpoints
├── technical_guides/       # Module-wise development instructions
├── requirements.txt        # Python dependency list
├── main.py                 # FastAPI Application entry-point
└── README.md
```

## 🛠️ Setup Instructions (WIP)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/selftaughtrahul/ai-assistant.git
    cd chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI server (development mode):**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000/`. You can view the interactive documentation at `http://localhost:8000/docs`.

---
*Note: This README is currently brief as the project is in its early stages. It will be expanded significantly as features are developed and the model is fine-tuned.*
