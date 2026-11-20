"""Explicitly reviewed historical riding-area map links."""

import json
from pathlib import Path

from .riding_area_maps import load_riding_area_maps


def load_event_map_associations():
    path = (
        Path(__file__).resolve().parent
        / "data/event_map_associations.json"
    )

    return json.loads(
        path.read_text(encoding="utf-8")
    )["associations"]


def maps_for_event(event_id):
    catalog = {
        item["original_filename"]: item
        for item in load_riding_area_maps()
    }

    return [
        catalog[link["original_filename"]]
        for link in load_event_map_associations()
        if link["event_id"] == event_id
    ]


def related_events_for_maps(events):
    by_id = {
        item["id"]: item
        for item in events
    }

    result = {}

    for link in load_event_map_associations():
        event = by_id.get(link["event_id"])

        if event is None:
            continue

        filename = link["original_filename"]

        result.setdefault(filename, []).append({
            "id": event["id"],
            "title": event["title"],
            "date_label": event["date_label"],
        })

    for related in result.values():
        related.sort(
            key=lambda item: item["id"],
            reverse=True,
        )

    return result
