# ui/components/controls.py
from __future__ import annotations

import streamlit as st

from models.game import Game
from services.storage import save
from ui.components.round_logic import apply_round_results, ensure_teams_allocated_once
from ui.components.validation import validate_placements
from ui.state import APP_STATE


def inject_button_css() -> None:
    st.markdown(
        """
        <style>
        .btn-vert .stButton>button { width: 100%; padding: 0.8rem 0; }
        .btn-vert .spacer { height: 10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_controls(game: Game, home_page_path: str = "ui/pages/home.py") -> None:
    inject_button_css()
    st.markdown('<div class="btn-vert">', unsafe_allow_html=True)

    ok, errs = validate_placements(game)
    new_round_disabled = not ok

    help_text = (
        "Cannot start new round:\n" + "\n".join(f"{e}" for e in errs)
        if not ok
        else None
    )

    clicked = st.button(
        "New round",
        key="btn_new_round",
        use_container_width=True,
        disabled=new_round_disabled,
        help=help_text,
    )
    if clicked:
        apply_round_results(game)
        try:
            save(game)
        except Exception as e:
            st.error(f"Save failed: {e}")

        # Allocate exactly once for the new round
        st.session_state["allocated_round"] = None  # invalidate previous round guard
        ensure_teams_allocated_once(game)
        st.rerun()

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    if st.button("Exit", key="btn_exit", use_container_width=True):
        try:
            save(game)
        except Exception as e:
            st.error(f"Save failed: {e}")
        st.switch_page(home_page_path)
        APP_STATE.game = None

    st.markdown("</div>", unsafe_allow_html=True)
