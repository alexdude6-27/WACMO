"""Published historical schedule listings, not confirmed ride results."""

from datetime import date
import json
from pathlib import Path

_SCHEDULE = (
    Path(__file__).parent / "data" / "legacy_schedule_2026.json"
)


def load_archived_schedule():
    """Return named archived listings, excluding drafts."""
    with _SCHEDULE.open(encoding="utf-8") as stream:
        source = json.load(stream)

    results = []
    seen = set()

    for entry in source["events"]:
        if (
            entry.get("publication_status") != "archived"
            or entry.get("needs_review")
            or entry.get("source_status") != "listed"
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
