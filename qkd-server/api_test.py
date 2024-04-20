from fastapi.testclient import TestClient
import pytest
from generate_key import app

client = TestClient(app)

def test_get_key():
    response = client.get("/key/64")
    print(response.json())
    assert response.status_code == 200
    assert "alice_key" in response.json()
    assert "bob_key" in response.json()
    assert "time_taken" in response.json()
    assert len(response.json()["alice_key"]) == 64
    assert len(response.json()["bob_key"]) == 64

