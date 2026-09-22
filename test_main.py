from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from fetcher import FetchError

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_check_returns_queued_job():
    with patch("main.fetch_page") as mock_fetch:
        mock_fetch.return_value = "<html></html>"
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
    with patch("main.fetch_page") as mock_fetch:
        mock_fetch.return_value = "<html></html>"
        create_response = client.post("/checks", json={"url": "https://example.com"})
        create_data = create_response.json()
        return_response = client.get(f"/checks/{create_data['id']}")
        return_data = return_response.json()
        assert return_response.status_code == 200
        assert return_data["id"] == create_data["id"]
        assert return_data["url"] == "https://example.com/"
        assert "created_at" in return_data


def test_get_check_with_unknown_id_returns_404():
    response = client.get("/checks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_create_check_with_reachable_page_marks_done():
    with patch("main.fetch_page") as mock_fetch:
        mock_fetch.return_value = "<html></html>"
        create_response = client.post("/checks", json={"url": "https://example.com"})
        create_data = create_response.json()
        return_response = client.get(f"/checks/{create_data['id']}")
        return_data = return_response.json()
        assert return_data["status"] == "done"
        mock_fetch.assert_called_once_with("https://example.com/")


def test_create_check_with_fetch_error_marks_failed():
    with patch("main.fetch_page") as mock_fetch:
        mock_fetch.side_effect = FetchError("http 404")
        create_result = client.post("/checks", json={"url": "https://example.com"})
        create_data = create_result.json()
        return_result = client.get(f"/checks/{create_data['id']}")
        return_data = return_result.json()
        assert return_data["status"] == "failed"
        assert return_data["error"] == "http 404"
        mock_fetch.assert_called_once_with("https://example.com/")
