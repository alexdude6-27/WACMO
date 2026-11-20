"""Grouped navigation and rolling historical archive."""

from datetime import date

from wacmo import create_app


def _client(monkeypatch, today):
    monkeypatch.setattr("wacmo.pacific_today", lambda: today)
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_grouped_navigation(monkeypatch):
    client = _client(monkeypatch, date(2026, 11, 20))
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    for group in ("About CMO", "Events", "Explore", "Resources"):
        assert group in html
    assert html.count('class="nav-group"') == 4
    assert 'href="/ride-flyers"' in html
    assert 'href="/riding-areas"' in html


def test_rolling_archive_2026(monkeypatch):
    client = _client(monkeypatch, date(2026, 11, 20))
    html = client.get("/events").get_data(as_text=True)

    for year in (2026, 2025, 2024):
        assert f"{year} Season" in html

    assert "2023 Season" not in html
    assert "18 schedule entries" in html
    assert "Fall Creek CMO" in html
    assert "Browse Earlier Years" in html


def test_rolling_archive_2027(monkeypatch):
    client = _client(monkeypatch, date(2027, 1, 2))
    html = client.get("/events").get_data(as_text=True)

    for year in (2027, 2026, 2025):
        assert f"{year} Season" in html
    assert "2024 Season" not in html


def test_older_year_selection(monkeypatch):
    client = _client(monkeypatch, date(2026, 11, 20))
    html = client.get(
        "/events?archive_year=2023"
    ).get_data(as_text=True)

    assert "2023 Season" in html
    assert "No structured events have been imported" in html


def test_invalid_older_year(monkeypatch):
    client = _client(monkeypatch, date(2026, 11, 20))
    for year in ("2024", "2010", "abc", "20230"):
        assert client.get(
            f"/events?archive_year={year}"
        ).status_code == 400
