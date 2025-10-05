# ui/pages/active_game.py
from __future__ import annotations

import streamlit as st

from models.game import Game
from ui.components.controls import render_controls
from ui.components.round_logic import ensure_round_attr, ensure_teams_allocated_once
from ui.components.scoreboard import show_scoreboard
from ui.components.team_viewer import inject_team_css, render_team_viewers
from ui.state import APP_STATE

st.set_page_config(layout="wide")

game: Game | None = APP_STATE.game
if not game:
    st.warning("No active game found.")
    st.stop()

# Layout
col_buttons, _, col_main, _, col_scoreboard = st.columns([2, 1, 6, 1, 4])


with col_main:
    st.title(f"{game.name}")
    ensure_round_attr(game)
    ensure_teams_allocated_once(game)
    inject_team_css()
    render_team_viewers(game)
    st.divider()

with col_buttons:
    render_controls(game, home_page_path="pages/home.py")  # adjust path if needed

with col_scoreboard:
    show_scoreboard(game)
