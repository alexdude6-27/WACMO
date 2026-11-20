"""Photo albums with optional WACMO event associations."""

import json
from pathlib import Path


def load_photo_albums():
    path = (
        Path(__file__).resolve().parent
        / "data/photo_albums.json"
    )

    return json.loads(
        path.read_text(encoding="utf-8")
    )["albums"]


def albums_for_event(event_id):
    return [
        album for album in load_photo_albums()
        if album.get("event_id") == event_id
    ]
