# ui/components/validation.py
from __future__ import annotations

from collections import Counter

import streamlit as st

from models.game import Game
from services.game import get_teams
from ui.components.team_viewer import placement_key


def iter_team_numbers(game: Game) -> list[int]:
    return [
        team_no for team_no, _ in sorted(get_teams(game).items(), key=lambda kv: kv[0])
    ]


def read_raw_placements(game: Game) -> dict[int, str]:
    return {
        team_no: str(st.session_state.get(placement_key(team_no, game), "")).strip()
        for team_no in iter_team_numbers(game)
    }


def validate_placements(game: Game) -> tuple[bool, list[str]]:
    errors: list[str] = []
    raw = read_raw_placements(game)

    # filled
    missing = [t for t, v in raw.items() if v == ""]
    if missing:
        errors.append(
            f"Enter a placement for all teams (missing: {', '.join(map(str, missing))})."
        )

    # integers
    non_int = [t for t, v in raw.items() if v and not v.isdigit()]
    if non_int:
        errors.append(
            f"Placements must be positive integers (check teams: {', '.join(map(str, non_int))})."
        )

    # unique (check only digits)
    numeric_vals = [int(v) for v in raw.values() if v.isdigit()]
    dup_counts = Counter(numeric_vals)
    dups = [str(p) for p, c in dup_counts.items() if c > 1]
    if dups:
        errors.append(
            f"Placements must be unique. Duplicate value(s): {', '.join(dups)}."
        )

    if min(numeric_vals, default=0) < 1 or max(numeric_vals, default=9) > 8:
        errors.append("Placements must be between 1 and 8.")

    return (len(errors) == 0, errors)


def placements_ready(game: Game) -> bool:
    ok, _ = validate_placements(game)
    return ok
