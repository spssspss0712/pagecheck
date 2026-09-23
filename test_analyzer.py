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


def test_analyze_page_with_meta_description_return_true():
    result = analyze_page(
        "<html><head><meta name='description' content='this is content'></head><body></body></html>"
    )
    assert result["has_meta_description"] is True


def test_analyze_page_without_meta_return_false():
    result = analyze_page("<html><head></head><body></body></html>")
    assert result["has_meta_description"] is False


def test_analyze_page_with_meta_no_description_with_content_return_false():
    result = analyze_page(
        "<html><head><meta name='title' content='this is content'></head><body></body></html>"
    )
    assert result["has_meta_description"] is False


def test_analyze_page_with_meta_description_no_content_return_false():
    result = analyze_page(
        "<html><head><meta name='description'></head><body></body></html>"
    )
    assert result["has_meta_description"] is False


def test_analyze_page_with_meta_description_with_empty_content_return_false():
    result = analyze_page(
        "<html><head><meta name='description' content='     '></head><body></body></html>"
    )
    assert result["has_meta_description"] is False
