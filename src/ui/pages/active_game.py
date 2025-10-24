# ui/pages/active_game.py
from __future__ import annotations

import streamlit as st

from models.game import Game
from ui.components.champion_view import champion_view
from ui.components.controls import render_controls
from ui.components.round_logic import ensure_round_attr, ensure_teams_allocated_once
from ui.components.scoreboard import show_scoreboard
from ui.components.team_viewer import inject_team_css, render_team_viewers
from ui.state import APP_STATE

st.set_page_config(page_title="Arena Grind", layout="wide")

game: Game | None = APP_STATE.game
if not game:
    st.warning("No active game found.")
    st.stop()

st.markdown('<div id="fixed-frame">', unsafe_allow_html=True)

# Layout
col_buttons, col_main, col_scoreboard = st.columns([3, 6, 3], gap="medium")


with col_main:
    if st.button(label="⟳ Refresh Champions", key="btn_refresh_champions"):
        with st.container():
            champion_view()

with col_buttons:
    st.title(f"{game.name}")
    ensure_round_attr(game)
    ensure_teams_allocated_once(game)
    inject_team_css()
    render_team_viewers(game)
    st.divider()
    render_controls(game, home_page_path="pages/home.py")  # adjust path if needed

with col_scoreboard:
    show_scoreboard(game)
