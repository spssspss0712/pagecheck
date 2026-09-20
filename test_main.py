from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_check_returns_queued_job():
    response = client.post("/checks", json={"url": "https://example.com"})
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["status"] == "queued"
    assert data["url"] == "https://example.com/"
    assert "created_at" in data


def test_create_check_with_invalid_url_returns_422():
    response = client.post("/checks", json={"url": "abcd"})
    assert response.status_code == 422


def test_get_check_returns_stored_record():
    create_response = client.post("/checks", json={"url": "https://example.com"})
    create_data = create_response.json()
    return_response = client.get(f"/checks/{create_data['id']}")
    return_data = return_response.json()
    assert return_response.status_code == 200
    assert return_data["id"] == create_data["id"]
    assert return_data["status"] == "queued"
    assert return_data["url"] == "https://example.com/"
    assert "created_at" in return_data


def test_get_check_with_unknown_id_returns_404():
    response = client.get("/checks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
