from textwrap import dedent

import streamlit as st

from models.game import Game
from services.game import get_teams

st.markdown(
    dedent("""
<style>
.team-badge {
  font-weight: 800; font-size: 1.05rem;
  width: 44px; height: 44px; border-radius: 8px;
  display: grid; place-items: center;
  background: rgba(0,0,0,0.05);
}
.player-stack { line-height: 1.35; }
.player-name { font-weight: 600; font-size: 1.05rem; }
.player-name.muted { opacity: 0.85; }
.row-spacer { height: 8px; }
</style>
"""),
    unsafe_allow_html=True,
)


def render_team_viewers(game: Game) -> None:
    teams = get_teams(game)  # {team_no: [Player, ...]}
    print(len(teams), "teams found:", teams)

    for team_no, players in sorted(teams.items(), key=lambda kv: kv[0]):
        name1 = players[0].name if len(players) > 0 else "—"
        name2 = players[1].name if len(players) > 1 else "—"

        # One horizontal row: [badge] [stacked names] [placement input]
        c_badge, c_names, c_input = st.columns([0.7, 3.0, 1.3])

        with c_badge:
            st.markdown(
                f'<div class="team-badge">{team_no}</div>', unsafe_allow_html=True
            )

        with c_names:
            st.markdown(
                f"""<div class="player-stack">
                        <div class="player-name">{name1}</div>
                        <div class="player-name muted">{name2}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

        with c_input:
            st.text_input(
                "Placement",
                key=f"placement_team_{team_no}",
                label_visibility="collapsed",
                placeholder="Placement",
            )

        # tiny spacer between rows
        st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)
