import streamlit as st

from models.game import Game
from services.storage import list_saved_games
from ui.state import APP_STATE


def _activate_and_go(game: Game) -> None:
    """Load the game, set it as active, and navigate."""
    APP_STATE.game = game
    st.switch_page("pages/active_game.py")


def load_game_component():
    st.subheader("Load a Saved Game")

    games = list_saved_games()

    if not games:
        st.info("No saved games found yet.")
        return

    for game in games:
        label = f"🗂️ {game.name} — {game.created_at}"
        if st.button(label, key=f"saved_{game.name}", use_container_width=True):
            _activate_and_go(game)
