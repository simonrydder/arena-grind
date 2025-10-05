from textwrap import dedent

import streamlit as st

from models.game import Game
from services.game import get_scoreboard


def show_scoreboard(game: Game):
    # Sort descending (highest score first)
    scoreboard = get_scoreboard(game)[::-1]

    # Distinct scores (high → low)
    scores_desc = sorted({p.score for p in scoreboard}, reverse=True)

    # --- Competition ranking: 1,1,3,3,5,... ---
    score_to_rank: dict[int, int] = {}
    rank = 1
    i = 0
    while i < len(scores_desc):
        score = scores_desc[i]
        score_to_rank[score] = rank
        # Skip all players with this same score
        same_score_count = sum(1 for p in scoreboard if p.score == score)
        rank += same_score_count
        i += 1

    # Determine medal class based on score value
    def row_class_for_score(score: int) -> str:
        if score == scores_desc[0]:
            return "first"
        if len(scores_desc) > 1 and score == scores_desc[1]:
            return "second"
        if len(scores_desc) > 2 and score == scores_desc[2]:
            return "third"
        return ""

    st.markdown("## 🏆 Scoreboard")

    rows = []
    for player in scoreboard:
        place_num = score_to_rank[player.score]
        row_class = row_class_for_score(player.score)
        rows.append(
            f'<tr class="{row_class}">'
            f'<td class="place">{place_num}.</td>'
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
        border: none !important;
        background-color: transparent;
        font-weight: 500;
    }}
    .scoreboard .place {{ text-align: right; width: 3ch; }}
    .scoreboard .name  {{ text-align: left; }}
    .scoreboard .score {{ text-align: left; padding-left: 1rem; }}

    /* Default (non-top-3) rows */
    .scoreboard tr:not(.first):not(.second):not(.third) td {{
        font-size: 1.1rem;
    }}

    /* Medal rows */
    .scoreboard tr.first  td {{ font-size: 1.6rem; font-weight: 800; color: #FFD700; }} /* gold */
    .scoreboard tr.second td {{ font-size: 1.4rem; font-weight: 700; color: #A7A7AD; }} /* silver */
    .scoreboard tr.third  td {{ font-size: 1.3rem; font-weight: 700; color: #A77044; }} /* bronze */
    </style>

    <table class="scoreboard">
        {"".join(rows)}
    </table>
    """)

    st.markdown(table_html, unsafe_allow_html=True)
