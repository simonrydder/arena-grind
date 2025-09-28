import streamlit as st

from models.game import Game


class State:
    @property
    def show_new(self) -> bool:
        return bool(st.session_state.get("show_new", False))

    @show_new.setter
    def show_new(self, v: bool) -> None:
        st.session_state["show_new"] = v

    @property
    def show_load(self) -> bool:
        return bool(st.session_state.get("show_load", False))

    @show_load.setter
    def show_load(self, v: bool) -> None:
        st.session_state["show_load"] = v

    @property
    def game(self) -> Game | None:
        return st.session_state.get("game", None)

    @game.setter
    def game(self, v: Game) -> None:
        st.session_state["game"] = v

    @property
    def active_page(self) -> str:
        return str(st.session_state.get("active_page", "pages/app.py"))

    @active_page.setter
    def active_page(self, v: str) -> None:
        st.session_state["active_page"] = v


APP_STATE = State()
