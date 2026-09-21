import httpx


class FetchError(Exception):
    pass


def fetch_page(url: str) -> str:
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
    except httpx.TimeoutException as e:
        raise FetchError("timeout after 10s") from e
    if response.status_code >= 400:
        raise FetchError(f"http {response.status_code}")
    if "text/html" not in response.headers.get("content-type", ""):
        raise FetchError("page is not html")
    return response.text
