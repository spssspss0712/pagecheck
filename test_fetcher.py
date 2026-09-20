from unittest.mock import patch, Mock
from fetcher import fetch_page, FetchError
import pytest, httpx


def test_fetch_page_with_html_response_returns_body():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, text="fake page")
        assert fetch_page("http://example.com") == "fake page"
        mock_get.assert_called_once()


def test_fetch_page_timeout_raises_fetch_error():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.side_effect = httpx.TimeoutException("timed out")
        with pytest.raises(FetchError):
            fetch_page("http://example.com")
        mock_get.assert_called_once()
