import streamlit as st

from models.game import Game
from models.player import Player
from ui.state import APP_STATE


def toggle_new_game_component():
    APP_STATE.show_new = not APP_STATE.show_new

    if APP_STATE.show_new:
        APP_STATE.show_load = False


def toggle_load_game_component():
    APP_STATE.show_load = not APP_STATE.show_load

    if APP_STATE.show_load:
        APP_STATE.show_new = False


def create_new_game():
    game_name = get_game_name()
    players = get_players()
    print(f"Creating new game: {game_name} with players: {players}")
    APP_STATE.game = Game(name=game_name, players=players)

    APP_STATE.active_page = "pages/active_game.py"
    print(f"Switching to page: {APP_STATE.active_page}")


def _search_player_names() -> list[str]:
    # keep only keys like player_<num>_name
    player_keys = [
        k
        for k in st.session_state.keys()
        if isinstance(k, str) and k.startswith("player_") and k.endswith("_name")
    ]

    # sort numerically by the <num> part
    player_keys.sort(key=lambda k: int(k.split("_")[1]))

    # collect non-empty names
    return [st.session_state[k] for k in player_keys if st.session_state.get(k)]


def get_players() -> list[Player]:
    return [Player(name=name, score=0, team=0) for name in _search_player_names()]


def get_game_name() -> str:
    game_name = st.session_state.get("game_name", "")

    if not game_name:
        st.error("Please enter a game name.")

    return game_name
