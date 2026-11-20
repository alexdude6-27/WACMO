"""Original published WACMO riding-area map catalog."""

import json
from pathlib import Path


def load_riding_area_maps():
    path = (
        Path(__file__).resolve().parent
        / "data/riding_area_maps.json"
    )

    return json.loads(
        path.read_text(encoding="utf-8")
    )["maps"]
