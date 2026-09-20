from unittest.mock import patch, Mock
import fetcher


def test_fetch_page_with_html_response_returns_body():
    with patch("fetcher.httpx.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, text="fake page")
        assert fetcher.fetch_page("http://example.com") == "fake page"
        mock_get.assert_called_once()
