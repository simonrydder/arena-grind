from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from models.game import Game
from models.player import Player

SAVE_DIR = Path("src/data/saves")


def _safe_filename(name: str) -> str:
    return name.replace(" ", "_")


def _to_jsonable(obj: Any) -> Any:
    """Convert dataclasses and datetimes to JSON-friendly structures."""
    if is_dataclass(obj) and not isinstance(obj, type):
        d = asdict(obj)
        # post-process any datetimes inside the top-level dataclass
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
        return d
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def save(game: Game) -> None:
    """
    Serialize the Game to JSON and store it under saves/<name>.json.
    Uses an atomic write to avoid partial files.
    """
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    filename = _safe_filename(game.name) + ".json"
    path = SAVE_DIR / filename

    data = _to_jsonable(game)

    tmp_path = path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
    tmp_path.replace(path)

    print(f"Game saved to {path}: {game}")


def load(name: str) -> Game:
    """
    Load a Game by name from saves/<name>.json.
    Gracefully reconstructs Player objects and 'created_at' if present.
    """
    filename = _safe_filename(name) + ".json"
    path = SAVE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No saved game found at {path}")

    with path.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    players = [Player(**p) for p in data.get("players", [])]

    game_name = data.get("name", name)
    round_number = data.get("round", 0)

    raw_created = data.get("created_at")
    if isinstance(raw_created, str):
        # handles ISO strings saved via isoformat()
        created_at = datetime.fromisoformat(raw_created)
    elif isinstance(raw_created, (int, float)):
        # just in case you ever store timestamps
        created_at = datetime.fromtimestamp(raw_created)
    elif isinstance(raw_created, datetime):
        created_at = raw_created
    else:
        # older saves without created_at
        created_at = datetime.now()

    return Game(
        name=game_name,
        players=players,
        round=round_number,
        created_at=created_at,
    )


def list_saved_games() -> list[Game]:
    """
    List all saved games (loaded as Game objects).
    """
    if not SAVE_DIR.exists():
        return []
    return [load(p.stem) for p in SAVE_DIR.glob("*.json")]
