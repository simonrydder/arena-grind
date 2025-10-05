from textwrap import dedent

import streamlit as st

from models.game import Game
from services.game import get_scoreboard


def _get_row_class(idx: int) -> str:
    if idx == 1:
        return "first"

    if idx == 2:
        return "second"

    if idx == 3:
        return "third"

    return ""


def show_scoreboard(game: Game):
    # Reverse order if you want highest score first
    scoreboard = get_scoreboard(game)[::-1]

    st.markdown("## 🏆 Scoreboard")

    rows = []
    for idx, player in enumerate(scoreboard, start=1):
        row_class = _get_row_class(idx)
        rows.append(
            f'<tr class="{row_class}">'
            f'<td class="place">{idx}.</td>'
            f'<td class="name">{player.name}</td>'
            f'<td class="score">{player.score}</td>'
            f"</tr>"
        )

    table_html = dedent(f"""
    <style>
    .scoreboard {{
        width: 100%;
        border-collapse: collapse;
        background-color: transparent;
    }}
    .scoreboard td {{
        padding: 6px 10px;
        border: none !important;          /* remove grid lines */
        background-color: transparent;    /* remove gray cells */
    }}
    .scoreboard .place {{
        text-align: right;
        width: 3ch;
    }}
    .scoreboard .name {{
        text-align: left;
    }}
    .scoreboard .score {{
        text-align: left;
        padding-left: 1rem;
    }}
    .scoreboard tr:not(.first):not(.second):not(.third) td {{
        font-size: 1.1rem;
    }}
    .scoreboard tr.first td {{
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFD700; /* gold color for 1st place */
    }}
    .scoreboard tr.second td {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #A7A7AD; /* silver color for 1st place */
    }}
    .scoreboard tr.third td {{
        font-size: 1.4rem;
        font-weight: 700;
        color: #A77044; /* bronze color for 1st place */
    }}
    </style>
    <table class="scoreboard">
        {"".join(rows)}
    </table>
    """)

    st.markdown(table_html, unsafe_allow_html=True)
