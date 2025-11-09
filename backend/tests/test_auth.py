from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_register_and_login():
    user = {"email": "a@b.com", "password": "123456"}
    client.post("/auth/register", json=user)
    res = client.post("/auth/login", json=user)
    assert res.status_code == 200
    assert "access_token" in res.json()
