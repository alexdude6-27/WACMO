"""Searchable historical PDF flyer archive."""

from pathlib import Path

from wacmo import create_app
from wacmo.event_flyers import load_event_flyers
from wacmo.events_archive import load_archived_schedule


ROOT = Path(__file__).resolve().parents[1]


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_archive_contains_verified_event_documents():
    documents = load_event_flyers()
    events = {
        item["id"] for item in load_archived_schedule()
    }

    assert len(documents) == 44
    assert sum(len(v) for v in documents.values()) == 45
    assert set(documents).issubset(events)

    for originals in documents.values():
        for original in originals:
            relative = Path(original["path"])
            preview = (
                ROOT / "wacmo/static/flyer_previews"
                / relative.relative_to("flyers")
            ).with_suffix(".jpg")

            assert preview.is_file()
            assert preview.read_bytes().startswith(
                bytes.fromhex("ffd8")
            )


def test_archive_page_has_seasons_and_previews():
    response = client().get("/ride-flyers")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "44 historical events" in html
    assert "45 original PDFs" in html
    assert "2026 Season" in html
    assert "2025 Season" in html
    assert "2024 Season" in html
    assert 'name="q"' in html
    assert 'name="year"' in html
    assert html.count('aria-current="page"') == 1
    assert html.count('aria-current="true"') == 1
    assert "flyer_previews/2025/" in html


def test_filter_by_year():
    response = client().get("/ride-flyers?year=2024")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="flyer-year-2024"' in html
    assert 'id="flyer-year-2025"' not in html
    assert 'id="flyer-year-2026"' not in html
    assert "2024-09-28-taylor-mountain.pdf" in html


def test_search_by_ride_and_location():
    browser = client()

    result = browser.get(
        "/ride-flyers?year=2025&q=Taylor"
    )

    html = result.get_data(as_text=True)
    assert result.status_code == 200
    assert "Original flyer" in html
    assert "Alternate flyer" in html
    assert "2025-04-26-taylor-mountain-2.pdf" in html
    assert "2024 Season" not in html

    location = browser.get("/ride-flyers?q=Hobart")
    assert location.status_code == 200
    assert "Taylor Mountain" in location.get_data(
        as_text=True
    )


def test_search_empty_and_invalid_year():
    browser = client()

    empty = browser.get(
        "/ride-flyers?q=unlikely-never-existing-ride"
    )

    assert empty.status_code == 200
    assert "No matching flyers" in empty.get_data(
        as_text=True
    )

    assert browser.get(
        "/ride-flyers?year=2035"
    ).status_code == 400


def test_original_2026_archive_is_still_available():
    response = client().get("/ride-flyers")
    html = response.get_data(as_text=True)

    assert '<details class="flyer-original-archive' in html
    assert "2026AwardsBanquet.pdf" in html
    assert "Schedule2026.pdf" in html


def test_preview_and_original_pdf_are_served():
    browser = client()

    preview = browser.get(
        "/static/flyer_previews/2025/"
        "2025-04-26-taylor-mountain.jpg"
    )

    assert preview.status_code == 200
    assert preview.data.startswith(
        bytes.fromhex("ffd8")
    )

    pdf = browser.get(
        "/static/flyers/2025/"
        "2025-04-26-taylor-mountain.pdf"
    )

    assert pdf.status_code == 200
    assert pdf.data.startswith(b"%PDF-")
