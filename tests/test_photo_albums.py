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

    assert len(albums) == 1

    album = albums[0]

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
