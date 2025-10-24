import streamlit as st

from ui.callbacks.click import toggle_load_game_component, toggle_new_game_component
from ui.components.load_game import load_game_component
from ui.components.new_game import new_game_component
from ui.state import APP_STATE

st.set_page_config(page_title="Arena Grind", layout="centered")


st.title("Welcome To Arena Grind")
st.caption("Hail warriors! Let the beat of war drums spur you to action!")

st.divider()


# New Game button + section
st.button(
    "New Game",
    key="new_game_button",
    on_click=toggle_new_game_component,
    use_container_width=True,
)
if APP_STATE.show_new:
    with st.container(border=True):
        new_game_component()


# Load Game button + section
st.button(
    "Load Game",
    key="load_game_button",
    on_click=toggle_load_game_component,
    use_container_width=True,
)
if APP_STATE.show_load:
    with st.container(border=True):
        load_game_component()
