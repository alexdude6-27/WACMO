"""Original flyers associated with WACMO events."""

import json
from pathlib import Path


def load_event_flyers():
    path = (
        Path(__file__).resolve().parent
        / "data/event_flyers.json"
    )

    payload = json.loads(
        path.read_text(encoding="utf-8")
    )

    return payload["events"]
