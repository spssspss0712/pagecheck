from unittest.mock import patch, Mock
from fetcher import fetch_page, FetchError
import pytest
import httpx


def test_fetch_page_with_html_response_returns_body():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            text="fake page",
            headers={"content-type": "text/html; charset=utf-8"},
        )
        assert fetch_page("http://example.com") == "fake page"
        mock_get.assert_called_once()


def test_fetch_page_with_timeout_raises_fetch_error():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.side_effect = httpx.TimeoutException("timed out")
        with pytest.raises(FetchError):
            fetch_page("http://example.com")
        mock_get.assert_called_once()


def test_fetch_page_with_server_error_raises_fetch_error():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.return_value = Mock(status_code=404, text="page not found")
        url = "http://example.com"
        with pytest.raises(FetchError):
            fetch_page(url)
        mock_get.assert_called_once_with(url, timeout=10.0, follow_redirects=True)


def test_fetch_page_with_non_html_content_type_raises_fetch_error():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200, text="pdf", headers={"content-type": "application/pdf"}
        )
        url = "http://example.com"
        with pytest.raises(FetchError):
            fetch_page(url)
        mock_get.assert_called_once_with(url, timeout=10.0, follow_redirects=True)


def test_fetch_page_with_connection_error_raises_fetch_error():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.side_effect = httpx.ConnectError("can not connect")
        url = "http://example.com"
        with pytest.raises(FetchError):
            fetch_page(url)
        mock_get.assert_called_once_with(url, timeout=10.0, follow_redirects=True)
