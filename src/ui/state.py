from typing import Iterator, Sequence

import streamlit as st

from models.champion import Champion
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
    def game(self, v: Game | None) -> None:
        st.session_state["game"] = v

    @property
    def active_page(self) -> str:
        return str(st.session_state.get("active_page", "pages/app.py"))

    @active_page.setter
    def active_page(self, v: str) -> None:
        st.session_state["active_page"] = v

    @property
    def champions(self) -> Sequence[Champion] | None:
        return st.session_state.get("champions", None)

    @champions.setter
    def champions(self, v: Sequence[Champion] | None) -> None:
        st.session_state["champions"] = v

    @property
    def tag(self) -> str | None:
        return st.session_state.get("tag", None)

    @tag.setter
    def tag(self, v: str | None) -> None:
        st.session_state["tag"] = v

    @property
    def tag_iterator(self) -> Iterator[tuple[Sequence[Champion], str]] | None:
        return st.session_state.get("tag_iterator", None)

    @tag_iterator.setter
    def tag_iterator(self, v: Iterator[tuple[Sequence[Champion], str]] | None) -> None:
        st.session_state["tag_iterator"] = v


APP_STATE = State()
