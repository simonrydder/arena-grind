import streamlit as st


def fixed_width_layout(
    total_width: int = 1220,
    column_widths: tuple[int, int, int] = (240, 680, 300),
    gap: str = "1.5rem",
):
    """
    Apply a fixed-width layout container and return Streamlit columns inside it.

    Args:
        total_width: total width of the page container in px
        column_widths: tuple of pixel widths for each column
        gap: horizontal gap between columns (CSS length, e.g., '1.5rem' or '20px')

    Returns:
        Tuple of Streamlit column objects, e.g. (col1, col2, col3)
    """
    css = f"""
    <style>
    #fixed-frame {{
        width: {total_width}px;
        margin: 0 auto;
    }}
    #fixed-frame [data-testid="stHorizontalBlock"] {{ gap: {gap}; }}
    """

    for i, w in enumerate(column_widths, start=1):
        css += f"""
        #fixed-frame [data-testid="column"]:nth-of-type({i}) {{
            flex: 0 0 {w}px !important;
            min-width: {w}px;
        }}
        """

    css += """
    .block-container { max-width: none; }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.markdown('<div id="fixed-frame">', unsafe_allow_html=True)
    cols = st.columns([1] * len(column_widths), gap="large")
    return cols
