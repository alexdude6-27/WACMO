"""Published WACMO historical map archive."""

from hashlib import sha256
from pathlib import Path

from wacmo import create_app
from wacmo.riding_area_maps import load_riding_area_maps


ROOT = Path(__file__).resolve().parents[1]


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_published_maps_are_preserved():
    records = load_riding_area_maps()

    assert len(records) == 26
    assert len({
        item["original_filename"].casefold()
        for item in records
    }) == 26

    for item in records:
        pdf = ROOT / "wacmo/static" / item["pdf_path"]
        preview = ROOT / "wacmo/static" / item["preview_path"]
        zoom = ROOT / "wacmo/static" / item["zoom_path"]

        assert pdf.is_file()
        assert preview.is_file()
        assert zoom.is_file()

        assert sha256(
            pdf.read_bytes()
        ).hexdigest() == item["pdf_sha256"]

        assert sha256(
            preview.read_bytes()
        ).hexdigest() == item["preview_sha256"]


def test_maps_page_has_all_published_areas():
    response = client().get("/riding-areas")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert html.count('class="riding-map-card"') == 26
    assert "Showing 26" in html
    assert "Norse Peak Wilderness" in html
    assert "View the original WACMO Maps page" in html
    assert "wacmo-photo-lightbox" in html
    assert "View Printable PDF" in html


def test_maps_search():
    browser = client()

    response = browser.get("/riding-areas?q=Ahtanum")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert html.count('class="riding-map-card"') == 1
    assert "Showing 1 of 26" in " ".join(html.split())

    response = browser.get(
        "/riding-areas?q=unlikely-map-name-999"
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'class="riding-map-card"' not in html
    assert "No maps match your search" in html


def test_published_map_assets_are_served():
    item = load_riding_area_maps()[0]
    browser = client()

    pdf = browser.get(
        "/static/" + item["pdf_path"]
    )

    assert pdf.status_code == 200
    assert pdf.data.startswith(b"%PDF-")

    preview = browser.get(
        "/static/" + item["preview_path"]
    )

    assert preview.status_code == 200


def test_unlisted_course_files_are_not_imported():
    assert not (
        ROOT / "wacmo/static/riding_maps/pdfs/"
        "2021DanvilleClues.pdf"
    ).exists()

    assert not (
        ROOT / "wacmo/static/riding_maps/pdfs/"
        "2021DanvilleMap.pdf"
    ).exists()
