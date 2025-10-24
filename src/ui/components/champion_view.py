import streamlit as st

from models.champion import Champion
from stategies.champion_selection import tag_selection
from ui.state import APP_STATE


def champion_view(columns: int = 12) -> None:
    game = APP_STATE.game
    if not game:
        st.warning("No active game found.")
        return

    # How many columns for the button grid inside the expander
    btn_cols = max(1, columns // 2 + 1)

    if not hasattr(APP_STATE, "tag_iterator") or APP_STATE.tag_iterator is None:
        APP_STATE.tag_iterator = tag_selection(game)
    # Optional: show how many are currently disabled in the header
    champions, tag = next(APP_STATE.tag_iterator)
    APP_STATE.champions = champions
    APP_STATE.tag = tag

    print(APP_STATE.champions)
    disabled_count = sum(1 for c in APP_STATE.champions if not c.available)
    expander_label = (
        f"Disable Champions ({disabled_count})"
        if disabled_count
        else "Disable Champions"
    )

    with st.expander(expander_label, expanded=False):
        cols = st.columns(btn_cols, gap="small")
        for i, champ in enumerate(APP_STATE.champions):
            with cols[i % btn_cols]:
                champion_button(champ)

    st.markdown(f"## Champion Availability - {APP_STATE.tag}")
    cols = st.columns(columns, gap="small")
    for i, champ in enumerate(APP_STATE.champions):
        with cols[i % columns]:
            champion_image(champ)


def champion_button(champ: Champion) -> None:
    symbol = "🟢" if champ.available else "🔴"
    label = f"{symbol} {champ.name[:6]}"
    st.button(
        label,
        key=f"champion_{champ.name}_button",
        on_click=lambda: setattr(champ, "available", not champ.available),
    )


def champion_image(champ: Champion, image_size=65, row_gap=10) -> None:
    filter_style = "grayscale(0%)" if champ.available else "grayscale(100%)"

    html = f"""
    <div style="
        display:inline-block;
        margin-bottom:{row_gap}px;
        width:{image_size}px;
        height:{image_size}px;
        border-radius:10px;
        overflow:hidden;
    ">
        <img src="{champ.image_url}" alt="{champ.name}" title="{champ.name}"
             style="
                width:100%;
                height:100%;
                object-fit:cover;
                border-radius:10px;
                filter:{filter_style};
                transition:filter 0.2s ease;
                display:block;
             ">
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
