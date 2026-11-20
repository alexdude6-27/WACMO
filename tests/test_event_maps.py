"""Curated historical event-to-map relationships."""

from pathlib import Path

from wacmo import create_app
from wacmo.event_maps import (
    load_event_map_associations,
    maps_for_event,
)
from wacmo.riding_area_maps import load_riding_area_maps


ROOT = Path(__file__).resolve().parents[1]


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_curated_links_only_use_published_maps():
    links = load_event_map_associations()
    maps = load_riding_area_maps()

    published = {
        item["original_filename"]
        for item in maps
    }

    assert len(links) == 20
    assert len({
        item["original_filename"]
        for item in links
    }) == 6

    assert all(
        item["original_filename"] in published
        and item["map_type"] == "riding_area_reference"
        for item in links
    )


def test_matching_event_displays_reference_map():
    browser = client()

    response = browser.get(
        "/events/2026-06-13-green-mountain"
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Riding Area Reference Map" in html
    assert "2012-green-mt-belfair-wa.pdf" in html
    assert "View printable map PDF" in html
    assert "Find this map in the Maps library" in html
    assert "Photos from this Event" in html


def test_scatter_creek_map_and_no_false_mountain_match():
    browser = client()

    scatter = browser.get(
        "/events/2026-10-10-scatter-creek"
    ).get_data(as_text=True)

    assert "2022-scatter-creek.pdf" in scatter
    assert "Riding Area Reference Map" in scatter

    unrelated = browser.get(
        "/events/2026-04-25-taylor-mountain"
    ).get_data(as_text=True)

    assert "Riding Area Reference Map" not in unrelated

    assert maps_for_event(
        "2026-04-25-taylor-mountain"
    ) == []


def test_map_library_links_back_to_events():
    browser = client()

    html = browser.get(
        "/riding-areas?q=Scatter"
    ).get_data(as_text=True)

    assert "Related WACMO Events" in html
    assert "/events/2026-10-10-scatter-creek" in html
    assert "/events/2025-10-11-scatter-creek" in html


def test_event_links_do_not_publish_course_clues():
    links = load_event_map_associations()

    assert not any(
        "clue" in item["original_filename"].lower()
        for item in links
    )

    for item in links:
        assert (
            ROOT / "wacmo/static/riding_maps/pdfs"
            / item["original_filename"]
        ).is_file()
