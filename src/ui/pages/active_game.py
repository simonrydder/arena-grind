import streamlit as st

from ui.components.scoreboard import show_scoreboard
from ui.state import APP_STATE

st.set_page_config(layout="wide")


game = APP_STATE.game  # assuming stored earlier
if not game:
    st.warning("No active game found.")
    st.stop()

col_main, col_scoreboard = st.columns([3, 1])

with col_main:
    st.title(f"Active Game: {game.name}")


with col_scoreboard:
    show_scoreboard(game)
