# import streamlit as st

# from models.game import Game
# from services.game import get_champions_by_tag, get_unique_tags
# from ui.components.champion_view import champion_image

# st.set_page_config(page_title="Arena Grind", layout="wide")


# for tag in get_unique_tags(Game("", [])):
#     st.markdown(f"## Champion Availability - {tag}")
#     cols = st.columns(12, gap="small")
#     for i, champ in enumerate(get_champions_by_tag(Game("", []), tag)):
#         with cols[i % 12]:
#             champion_image(champ)
