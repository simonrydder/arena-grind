from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from models.game import Game
from models.player import Player

SAVE_DIR = Path("src/data/saves")


def _safe_filename(name: str) -> str:
    # keep it simple; make the filename predictable
    # (you can make this stricter if you expect special characters)
    return name.replace(" ", "_")


def save(game: Game) -> None:
    """
    Serialize the Game to JSON and store it under saves/<name>.json.
    Uses an atomic write to avoid partial files.
    """
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    filename = _safe_filename(game.name) + ".json"
    path = SAVE_DIR / filename

    data = asdict(game)  # handles nested dataclasses (players) out of the box

    # Atomic write: write to temp, then replace
    tmp_path = path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
    tmp_path.replace(path)

    print(f"Game saved to {path}: {game}")


def load(name: str) -> Game:
    """
    Load a Game by name from saves/<name>.json.
    Gracefully reconstructs Player objects and defaults round if missing.
    """
    filename = _safe_filename(name) + ".json"
    path = SAVE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No saved game found at {path}")

    with path.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    # Rebuild Player instances explicitly
    players_data = data.get("players", [])
    players = [Player(**p) for p in players_data]

    # Prefer stored name; fall back to the requested name
    game_name = data.get("name", name)
    round_number = data.get("round", 0)
    created_at = data.get("created_at", datetime.now())

    return Game(
        name=game_name,
        players=players,
        round=round_number,
        created_at=created_at,
    )


def list_saved_games() -> list[Game]:
    """
    List all saved game names (without .json suffix).
    """
    if not SAVE_DIR.exists():
        return []

    saved_games = []
    for file in SAVE_DIR.glob("*.json"):
        saved_games.append(load(file.stem))

    return saved_games
