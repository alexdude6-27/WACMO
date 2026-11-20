"""WACMO photo album foundation and preservation."""

from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import wacmo.photo_albums as photo_module
from wacmo import create_app


ROOT = Path(__file__).resolve().parents[1]


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_original_album_has_verified_photographs():
    albums = photo_module.load_photo_albums()

    originals = [
        album for album in albums
        if album["slug"] == "original-wacmo-ride-photos"
    ]

    assert len(originals) == 1

    album = originals[0]

    assert album["event_id"] is None
    assert album["year"] is None
    assert len(album["photos"]) == 12

    for photo in album["photos"]:
        path = ROOT / "wacmo/static" / photo["path"]

        assert path.is_file()
        assert sha256(
            path.read_bytes()
        ).hexdigest() == photo["sha256"]


def test_gallery_index():
    response = client().get("/galleries")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Photo Gallery" in html
    assert "Original WACMO Ride Photos" in html
    assert "Find WACMO on Facebook" in html
    assert "/galleries/original-wacmo-ride-photos" in html
    assert "View the original WACMO photo gallery page" in html


def test_gallery_detail_and_missing_album():
    browser = client()

    response = browser.get(
        "/galleries/original-wacmo-ride-photos"
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "12 original photographs" in html
    assert html.count("photo-image-grid") >= 1
    assert "/static/photos/original-wacmo-ride-photos/" in html

    assert browser.get(
        "/galleries/not-a-real-album"
    ).status_code == 404


def test_original_photo_is_served():
    response = client().get(
        "/static/photos/original-wacmo-ride-photos/IMG005.JPG"
    )

    assert response.status_code == 200
    assert response.data.startswith(bytes.fromhex("ffd8"))


def test_unlinked_photos_do_not_appear_on_event():
    html = client().get(
        "/events/2026-04-25-taylor-mountain"
    ).get_data(as_text=True)

    assert "event-photo-albums" not in html


def test_optional_event_album_preview(monkeypatch):
    album = deepcopy(
        photo_module.load_photo_albums()[0]
    )

    album["event_id"] = "2026-04-25-taylor-mountain"

    monkeypatch.setattr(
        photo_module,
        "load_photo_albums",
        lambda: [album],
    )

    browser = client()

    response = browser.get(
        "/events/2026-04-25-taylor-mountain"
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'class="event-photo-albums"' in html
    assert "/galleries/original-wacmo-ride-photos" in html
    assert "View all 12" in html

    album_response = browser.get(
        "/galleries/original-wacmo-ride-photos"
    )

    assert "View the related WACMO event" in (
        album_response.get_data(as_text=True)
    )


def test_facebook_albums_are_imported():
    albums = photo_module.load_photo_albums()

    slugs = {album["slug"] for album in albums}

    assert "green-mountain-2026-06-13" in slugs
    assert "scatter-creek-2026-10-10" in slugs
    assert "mt-pockets-2026-05-23" in slugs
    assert "teanaway-cmo-2026-09-12" in slugs
    assert "danville-georgetown-cmo-2022-10-15" in slugs
    assert "sahara-creek-2021-07-24" in slugs

    by_slug = {
        album["slug"]: album for album in albums
    }

    assert len(by_slug["green-mountain-2026-06-13"]["photos"]) == 4
    assert len(by_slug["scatter-creek-2026-10-10"]["photos"]) == 3
    assert len(by_slug["mt-pockets-2026-05-23"]["photos"]) == 8
    assert len(by_slug["teanaway-cmo-2026-09-12"]["photos"]) == 3
    assert len(by_slug["danville-georgetown-cmo-2022-10-15"]["photos"]) == 2
    assert len(by_slug["sahara-creek-2021-07-24"]["photos"]) == 3

def test_facebook_album_photos_exist():
    albums = photo_module.load_photo_albums()

    targets = [
        album for album in albums
        if album["slug"] != "original-wacmo-ride-photos"
    ]

    assert len(targets) == 6

    for album in targets:
        for photo in album["photos"]:
            path = ROOT / "wacmo/static" / photo["path"]
            assert path.is_file()
            assert sha256(
                path.read_bytes()
            ).hexdigest() == photo["sha256"]

def test_event_pages_show_facebook_album_previews():
    browser = client()

    checks = {
        "/events/2026-06-13-green-mountain":
            "green-mountain-2026-06-13",
        "/events/2026-10-10-scatter-creek":
            "scatter-creek-2026-10-10",
        "/events/2026-05-23-m-t-pockets":
            "mt-pockets-2026-05-23",
        "/events/2026-09-12-teanaway-indian-camp":
            "teanaway-cmo-2026-09-12",
    }

    for route, slug in checks.items():
        response = browser.get(route)
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert 'class="event-photo-albums"' in html
        assert f"/galleries/{slug}" in html

def test_gallery_albums_newest_first():
    response = client().get("/galleries")
    html = response.get_data(as_text=True)

    assert response.status_code == 200

    slugs = [
        "scatter-creek-2026-10-10",
        "teanaway-cmo-2026-09-12",
        "green-mountain-2026-06-13",
        "mt-pockets-2026-05-23",
        "danville-georgetown-cmo-2022-10-15",
        "sahara-creek-2021-07-24",
        "original-wacmo-ride-photos",
    ]

    positions = [
        html.index(f'href="/galleries/{slug}"')
        for slug in slugs
    ]

    assert positions == sorted(positions)
    assert "2026 Season" in html
    assert "2022 Season" in html
    assert "2021 Season" in html


def test_gallery_index_shows_facebook_albums():
    response = client().get("/galleries")
    html = response.get_data(as_text=True)

    assert "Green Mountain" in html
    assert "Scatter Creek" in html
    assert "MT Pockets" in html
    assert "Teanaway CMO" in html
    assert "Danville-Georgetown CMO" in html
    assert "Sahara Creek" in html
