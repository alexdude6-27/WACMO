"""WACMO page-title typography and event layout."""

from pathlib import Path

from wacmo import create_app


ROOT = Path(__file__).resolve().parents[1]


def test_shared_page_titles_use_original_rye_font():
    css = (
        ROOT / "wacmo/static/css/site.css"
    ).read_text(encoding="utf-8")

    assert 'font-family: "WACMO Rye", Georgia, serif;' in css
    assert ".calendar-heading h2," in css
    assert ".history-heading h2 {" in css
    assert "color: #422817;" in css


def test_event_detail_is_compact():
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get(
        "/events/2026-05-23-m-t-pockets"
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "MT Pockets" in html
    assert 'class="page-intro event-detail-intro"' in html
    assert (
        'class="content-section container event-detail-content"'
        in html
    )
    assert (
        'class="heritage-article event-detail-article"'
        in html
    )


def test_compact_styles_are_scoped_to_event_pages():
    css = (
        ROOT / "wacmo/static/css/site.css"
    ).read_text(encoding="utf-8")

    assert ".content-section.event-detail-content {" in css
    assert ".heritage-article.event-detail-article {" in css
    assert ".event-detail-article p {" in css
