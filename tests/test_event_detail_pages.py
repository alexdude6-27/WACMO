"""Public WACMO ride pages, navigation and SEO metadata."""

from datetime import date

from wacmo import create_app


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_historical_ride_has_dedicated_page():
    response = client().get(
        "/events/2026-05-23-m-t-pockets"
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "MT Pockets" in html
    assert "Tenino, WA" in html
    assert '<meta name="robots" content="index,follow">' in html
    assert '<link rel="canonical"' in html
    assert '<meta name="description"' in html


def test_calendar_links_to_internal_event_pages():
    html = client().get(
        "/events?year=2026&month=5"
    ).get_data(as_text=True)

    assert 'href="/events/2026-05-23-m-t-pockets"' in html
    assert "ride_information.php" not in html


def test_missing_or_unpublished_event_is_404():
    for path in (
        "/events/does-not-exist",
        "/events/2026-06-27-unnamed-tentative-event",
    ):
        assert client().get(path).status_code == 404


def test_dropdown_not_initially_open():
    html = client().get("/events").get_data(as_text=True)
    assert '<details class="nav-group">' in html
    assert '<details class="nav-group" open>' not in html


def test_older_year_scroll_target(monkeypatch):
    monkeypatch.setattr(
        "wacmo.pacific_today",
        lambda: date(2026, 11, 20),
    )

    html = client().get(
        "/events?archive_year=2022"
    ).get_data(as_text=True)

    assert '#selected-archive-year"' in html
    assert 'id="selected-archive-year"' in html
    assert "2022 Season" in html
