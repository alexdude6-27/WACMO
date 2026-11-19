from datetime import date

import pytest

from wacmo import create_app
from wacmo.calendar import build_month


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_november_2026_calendar():
    month = build_month(
        2026, 11, date(2026, 11, 18)
    )

    assert month["title"] == "November 2026"
    assert len(month["weeks"]) == 5
    assert len(month["weeks"][0]) == 7
    assert month["weeks"][0][0]["iso"] == "2026-11-01"

    days = [
        day
        for week in month["weeks"]
        for day in week
    ]

    assert sum(
        day["in_month"] for day in days
    ) == 30

    assert sum(
        day["is_today"] for day in days
    ) == 1

    assert month["previous"] == (2026, 10)
    assert month["following"] == (2026, 12)


def test_leap_year():
    month = build_month(
        2028, 2, date(2028, 2, 29)
    )

    days = [
        day
        for week in month["weeks"]
        for day in week
    ]

    assert sum(
        day["in_month"] for day in days
    ) == 29


def test_calendar_year_boundaries():
    first = build_month(
        2000, 1, date(2026, 11, 18)
    )

    last = build_month(
        2100, 12, date(2026, 11, 18)
    )

    assert first["previous"] is None
    assert last["following"] is None


def test_calendar_page(client):
    response = client.get(
        "/events?year=2026&month=11"
    )

    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "November 2026" in body
    assert "No rides published" in body
    assert 'datetime="2026-11-18"' in body
    assert "year=2026&amp;month=10" in body
    assert "year=2026&amp;month=12" in body


def test_default_month_uses_pacific_date(
    client, monkeypatch
):
    monkeypatch.setattr(
        "wacmo.pacific_today",
        lambda: date(2026, 11, 18),
    )

    response = client.get("/events")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "November 2026" in body
    assert body.count('aria-current="date"') == 1


@pytest.mark.parametrize(
    "query",
    [
        "?year=2026",
        "?month=11",
        "?year=2026&month=13",
        "?year=1999&month=12",
        "?year=2026&month=abc",
        "?year=hello&month=11",
    ],
)
def test_invalid_month_requests(client, query):
    response = client.get("/events" + query)
    assert response.status_code == 400
