from analyzer import analyze_page


def test_analyze_page_with_title_return_true():
    result = analyze_page(
        "<html><head><title>This is title</title></head><body></body></html>"
    )
    assert result["has_title"] is True


def test_analyze_page_without_title_return_false():
    result = analyze_page("<html><head></head><body></body></html>")
    assert result["has_title"] is False


def test_analyze_page_with_empty_title_return_false():
    result = analyze_page("<html><head><title></title></head><body></body></html>")
    assert result["has_title"] is False


def test_analyze_page_with_space_title_return_false():
    result = analyze_page("<html><head><title>     </title></head><body></body></html>")
    assert result["has_title"] is False
