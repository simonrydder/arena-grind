import streamlit as st

st.set_page_config(page_title="Arena Grind", page_icon="⚔️", layout="centered")

# --- State init
if "show_new" not in st.session_state:
    st.session_state.show_new = False

if "show_load" not in st.session_state:
    st.session_state.show_load = False


# --- Callbacks
def toggle_new():
    st.session_state.show_new = not st.session_state.show_new


def toggle_load():
    st.session_state.show_load = not st.session_state.show_load


# --- UI
st.title("Welcome To Arena Grind")
st.caption("Hail warriors! Let the beat of war drums spur you to action!")

st.divider()


# New Game button + section
st.button(
    "New Game", key="new_game_button", on_click=toggle_new, use_container_width=True
)
if st.session_state.show_new:
    with st.container(border=True):
        st.subheader("Game Settings")
        st.text_input(
            "Game name",
            key="game_name",
            placeholder="Game Name",
            label_visibility="collapsed",
        )
        st.subheader("Players")
        cols = st.columns(4)
        for i in range(16):
            col = cols[i % 4]
            with col:
                st.text_input(
                    f"Player {i + 1}",
                    key=f"player_{i + 1}_name",
                    placeholder=f"Player {i + 1}",
                    label_visibility="collapsed",
                )


# Load Game button + section
st.button(
    "Load Game", key="load_game_button", on_click=toggle_load, use_container_width=True
)
if st.session_state.show_load:
    with st.container(border=True):
        st.subheader("Load a Saved Game")
        st.text_input("Enter save name or path", key="load_game_ref")
