"""Historical 2026 schedule import and calendar display."""

from wacmo import create_app
from wacmo.events_archive import load_archived_schedule


def test_archived_schedule_filters_tentative_and_drafts():
    entries = load_archived_schedule()

    assert len(entries) == 18
    assert all(
        e["publication_status"] == "archived"
        for e in entries
    )
    assert any(
        e["start_date"] == "2026-06-27"
        and e["title"] == "MT Pockets take 2"
        for e in entries
    )
    assert entries[0]["title"] == "Awards Banquet"


def test_historical_entries_render_in_month():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/events?year=2026&month=3")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "March 2026" in page
    assert "Danville-Georgetown" in page
    assert "Scatter Creek or Bust" in page
    assert "does not confirm the event took place" in page
    assert "unnamed-tentative-event" not in page


def test_multiday_event_is_visible_on_both_dates():
    app = create_app()
    app.config["TESTING"] = True

    page = app.test_client().get(
        "/events?year=2026&month=4"
    ).get_data(as_text=True)

    assert "Apr 11–12, 2026" in page
    assert page.count("Les Hilde") >= 3


def test_no_2026_events_after_october():
    app = create_app()
    app.config["TESTING"] = True

    page = app.test_client().get(
        "/events?year=2026&month=11"
    ).get_data(as_text=True)

    assert "No rides published for this month yet" in page
    assert "Awards Banquet" in page
    assert "2026 Season" in page


def test_nacmo_references_and_original_names():
    entries = load_archived_schedule()

    linked = [
        event for event in entries
        if event.get("nacmo_details_url")
    ]
    assert len(linked) == 16

    july = next(
        event for event in entries
        if event["start_date"] == "2026-07-10"
    )
    assert july["title"] == "Fall Creek CMO"
    assert july["wacmo_original"]["title"] == (
        "Margaret McKenny-Capitol Forest"
    )

    june = next(
        event for event in entries
        if event["start_date"] == "2026-06-27"
    )
    assert june["wacmo_original"]["source_status"] == "tentative"
    assert june["publication_status"] == "archived"

    app = create_app()
    app.config["TESTING"] = True
    page = app.test_client().get(
        "/events?year=2026&month=6"
    ).get_data(as_text=True)

    assert "MT Pockets take 2" in page
    assert "rdkey=20102093&amp;rikey=20101161" in page
