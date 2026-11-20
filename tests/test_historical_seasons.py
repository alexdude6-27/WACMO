"""2024 and 2025 historical WACMO event archives."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from wacmo import create_app
from wacmo.events_archive import load_archived_schedule
from wacmo.event_flyers import load_event_flyers


ROOT = Path(__file__).resolve().parents[1]


def test_historical_events_and_statuses():
    events = load_archived_schedule()

    counts = Counter(
        event["start_date"][:4]
        for event in events
    )

    assert counts["2026"] == 18
    assert counts["2025"] == 18
    assert counts["2024"] == 19

    assert len({
        event["id"] for event in events
    }) == len(events)

    cancelled = {
        event["id"]
        for event in events
        if event.get("event_status") == "cancelled"
    }

    assert cancelled == {
        "2024-09-14-sage-horse-camp",
        "2024-09-28-green-river-horse-camp",
    }

    extra = next(
        event for event in events
        if event["id"] == "2024-09-28-taylor-mountain"
    )

    assert extra["source_status"] == "flyer_only"


def test_restored_flyers_are_original():
    flyers = load_event_flyers()

    assert len(flyers) == 44
    assert sum(
        len(documents)
        for documents in flyers.values()
    ) == 45

    for documents in flyers.values():
        for document in documents:
            path = (
                ROOT / "wacmo/static"
                / document["path"]
            )

            assert path.is_file()
            assert (
                sha256(path.read_bytes()).hexdigest()
                == document["sha256"]
            )

    assert len(
        flyers["2025-04-26-taylor-mountain"]
    ) == 2

    # This scanned flyer still requires visual review.
    assert (
        "2024-08-10-south-seattle-saddle-club"
        not in flyers
    )


def test_historical_pages_and_calendar():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    for event_id in (
        "2025-05-10-rock-creek",
        "2024-09-28-taylor-mountain",
        "2024-09-14-sage-horse-camp",
    ):
        assert client.get(
            f"/events/{event_id}"
        ).status_code == 200

    flyer_only = client.get(
        "/events/2024-09-28-taylor-mountain"
    ).get_data(as_text=True)

    assert "Flyer-only historical listing" in flyer_only

    cancelled = client.get(
        "/events/2024-09-14-sage-horse-camp"
    ).get_data(as_text=True)

    assert "Cancelled" in cancelled

    taylor = client.get(
        "/events/2025-04-26-taylor-mountain"
    ).get_data(as_text=True)

    assert "Original flyer" in taylor
    assert "Alternate flyer" in taylor

    calendar = client.get(
        "/events?year=2024&month=9"
    ).get_data(as_text=True)

    assert "(Cancelled)" in calendar
    assert "(Flyer-only)" in calendar
    assert (
        "/events/2024-09-28-taylor-mountain"
        "#event-flyers"
    ) in calendar
