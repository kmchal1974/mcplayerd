"""State file writing support for McPlayerD."""

import json
import os
from pathlib import Path


STATE_PATH = Path("/run/mcplayer/state.json")


def write_state(state: dict, path: Path = STATE_PATH) -> None:
    """Write McPlayerD state atomically as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(".tmp")

    with temp_path.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, indent=2, ensure_ascii=False)
        state_file.write("\n")
        state_file.flush()
        os.fsync(state_file.fileno())

    os.replace(temp_path, path)