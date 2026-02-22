from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat():
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test-session", "text": "Hello, how are you?"}
    )
    print("Status:", response.status_code)
    print("Response:", response.json())
    
if __name__ == "__main__":
    test_chat()
