from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test Todo", "description": "This is a test todo."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo."
    assert data["completed"] is False