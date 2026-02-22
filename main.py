from fastapi import FastAPI
from routers import chat


app = FastAPI(
    title="Customer Support Chatbot",
    description="AI-Powered Customer Support Chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(chat.router,prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)