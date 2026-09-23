from bs4 import BeautifulSoup


def analyze_page(html_page: str) -> dict:
    soup = BeautifulSoup(html_page, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    result = {"has_title": True, "has_meta_description": True}

    if soup.title is None or soup.title.get_text(strip=True) == "":
        result["has_title"] = False

    content = meta.get("content") if meta else None
    if content is None or content.strip() == "":
        result["has_meta_description"] = False

    return result
