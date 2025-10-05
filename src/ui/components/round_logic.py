# ui/components/round_logic.py
from __future__ import annotations

import streamlit as st

from models.game import Game
from services.game import allocate_teams, update_team_score
from ui.components.team_viewer import placement_key
from ui.components.validation import iter_team_numbers


def ensure_round_attr(game: Game) -> None:
    if not hasattr(game, "round") or game.round is None:
        game.round = 1


def ensure_teams_allocated_once(game: Game) -> None:
    """
    Allocate teams at most once per game.round.
    Uses st.session_state['allocated_round'] as a guard.
    """
    ensure_round_attr(game)
    if st.session_state.get("allocated_round") != game.round:
        allocate_teams(game)
        st.session_state["allocated_round"] = game.round


def apply_round_results(game: Game) -> None:
    """
    Read validated placements, update scores for each team,
    and advance to next round. Round-scoped keys mean no clearing needed.
    """
    for team_no in iter_team_numbers(game):
        placement = int(st.session_state.get(placement_key(team_no, game), "0"))
        update_team_score(game, team_no, placement)
    game.round += 1
