import streamlit as st

from ui.callbacks.click import create_new_game


def _new_game_settings_component():
    st.subheader("Game Settings")
    st.text_input(
        "Game name",
        key="game_name",
        placeholder="Game Name",
        label_visibility="collapsed",
    )


def _new_player_component(idx: int) -> None:
    st.text_input(
        f"Player {idx + 1}",
        key=f"player_{idx + 1}_name",
        placeholder=f"Player {idx + 1}",
        label_visibility="collapsed",
    )


def _new_game_players_component(max_players: int, num_cols: int) -> None:
    st.subheader("Players")
    cols = st.columns(num_cols)
    for i in range(max_players):
        col = cols[i // num_cols]
        with col:
            _new_player_component(i)


def _new_game_create_game_component() -> None:
    if st.button(
        "Create Game",
        key="create_game_button",
        use_container_width=True,
        on_click=create_new_game,
    ):
        st.switch_page("pages/active_game.py")


def new_game_component():
    _new_game_settings_component()
    _new_game_players_component(max_players=16, num_cols=4)
    _new_game_create_game_component()
