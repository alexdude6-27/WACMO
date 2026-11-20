"""Published historical schedule listings, not confirmed ride results."""

from datetime import date
import json
from pathlib import Path

_SCHEDULE = (
    Path(__file__).parent / "data" / "legacy_schedule_2026.json"
)

_HISTORICAL_SCHEDULES = tuple(
    _SCHEDULE.with_name(f"legacy_schedule_{year}.json")
    for year in (2025, 2024)
)


def load_archived_schedule():
    """Return named archived listings, excluding drafts."""
    source_events = []

    for path in (_SCHEDULE, *_HISTORICAL_SCHEDULES):
        with path.open(encoding="utf-8") as stream:
            source_events.extend(json.load(stream)["events"])

    results = []
    seen = set()

    for entry in source_events:
        if (
            entry.get("publication_status") != "archived"
            or entry.get("needs_review")
            or entry.get("source_status") not in ("listed", "flyer_only")
        ):
            continue

        identifier = entry["id"]

        if identifier in seen:
            raise ValueError(
                f"Duplicate archive event: {identifier}"
            )
        seen.add(identifier)

        first = date.fromisoformat(entry["start_date"])
        last = date.fromisoformat(entry["end_date"])

        if last < first or not entry.get("title"):
            raise ValueError(
                f"Invalid archive event: {identifier}"
            )

        date_label = f"{first.strftime('%b')} {first.day}"

        if last != first:
            if last.month == first.month and last.year == first.year:
                date_label += f"–{last.day}"
            else:
                date_label += (
                    f"–{last.strftime('%b')} {last.day}"
                )

        date_label += f", {first.year}"

        results.append({
            **entry,
            "date_label": date_label,
        })

    return sorted(
        results,
        key=lambda event: (
            event["start_date"],
            event["id"],
        ),
    )
