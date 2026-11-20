"""Historical WACMO PDF flyer preservation."""

from hashlib import sha256
from pathlib import Path

from wacmo import create_app
from wacmo.event_flyers import load_event_flyers
from wacmo.events_archive import load_archived_schedule


ROOT = Path(__file__).resolve().parents[1]


def test_2026_flyers_reference_real_events():
    flyers = load_event_flyers()

    event_ids = {
        event["id"]
        for event in load_archived_schedule()
    }

    assert len(flyers) == 13
    assert set(flyers).issubset(event_ids)

    for event_id, documents in flyers.items():
        assert len(documents) >= 1

        for document in documents:
            path = (
                ROOT / "wacmo/static"
                / document["path"]
            )

            assert path.is_file(), event_id
            assert path.read_bytes().startswith(b"%PDF-")
            assert (
                sha256(path.read_bytes()).hexdigest()
                == document["sha256"]
            )


def test_ride_page_embeds_its_original_flyer():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get(
        "/events/2026-05-23-m-t-pockets"
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Original Event Flyer" in html
    assert 'class="event-flyer-frame"' in html
    assert (
        "/static/flyers/2026/"
        "2026-05-23-m-t-pockets.pdf"
    ) in html
    assert "Open original PDF" in html
    assert "Download flyer" in html


def test_archive_links_to_flyer_section():
    app = create_app()
    app.config["TESTING"] = True
    html = app.test_client().get(
        "/events?year=2026&month=5"
    ).get_data(as_text=True)

    assert (
        "/events/2026-05-23-m-t-pockets"
        "#event-flyers"
    ) in html
    assert "View flyer" in html


def test_events_without_flyers_have_no_pdf_viewer():
    app = create_app()
    app.config["TESTING"] = True

    html = app.test_client().get(
        "/events/2026-04-11-les-hilde-horse-camp"
    ).get_data(as_text=True)

    assert 'class="event-flyer-frame"' not in html
    assert "not yet been linked" in html


def test_original_pdf_is_served():
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get(
        "/static/flyers/2026/"
        "2026-05-23-m-t-pockets.pdf"
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
