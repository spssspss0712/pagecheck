from bs4 import BeautifulSoup


def analyze_page(html_page: str) -> dict:
    soup = BeautifulSoup(html_page, "html.parser")

    if soup.title is None or soup.title.get_text(strip=True) == "":
        return {"has_title": False}
    return {"has_title": True}
