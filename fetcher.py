import httpx


class FetchError(Exception):
    pass


def fetch_page(url: str):
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
    except httpx.TimeoutException as e:
        raise FetchError("timeout after 10s") from e

    # print(response.status_code)
    # print(response.text)
    # print(response.headers["content-type"])
    return response.text
