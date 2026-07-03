import base64
from pathlib import Path
import streamlit as st


PAGES = [
    "Home",
    "Vector Analysis",
    "Career Matches",
    "ATS Radar",
    "Growth Path",
    "Vector Boost",
    "Interview Launchpad",
]


def get_svg_base64(path: str) -> str:
    """Convert SVG file to base64 for inline display."""
    svg_path = Path(path)
    if svg_path.exists():
        with open(svg_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def nav_button(label):

    active = st.session_state.page == label

    if active:
        button_type = "primary"
    else:
        button_type = "secondary"

    if st.button(
        label,
        use_container_width=True,
        type=button_type,
    ):
        st.session_state.page = label
        st.rerun()


def render_sidebar():

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    with st.sidebar:

        # Logo
        logo_b64 = get_svg_base64("assets/images/logo_cv.svg")

        if logo_b64:
            st.markdown(
                f"""
                <div style="text-align:center; padding-top:16px; padding-bottom:8px;">
                    <img src="data:image/svg+xml;base64,{logo_b64}"
                         width="90"
                         style="border-radius:50%; margin-bottom:10px;"/>
                    <h1 style="
                        color:#DC2626;
                        font-size:28px;
                        margin:0;
                        font-weight:900;
                        letter-spacing:-0.5px;
                    ">CareerVector</h1>
                    <p style="
                        color:#6B7280;
                        margin-top:4px;
                        font-size:13px;
                    ">Navigate Your Career.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Fallback if logo file not found
            st.markdown(
                """
                <div style="text-align:center; padding-top:10px; padding-bottom:15px;">
                    <h1 style="
                        color:#DC2626;
                        font-size:40px;
                        margin-bottom:0;
                        font-weight:800;
                    ">CareerVector</h1>
                    <p style="color:#6B7280; margin-top:4px;">
                        Navigate Your Career.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        for page in PAGES:
            nav_button(page)

        st.divider()

        st.info(
            "Upgrade to CareerVector Pro\n\n"
            "Unlock premium AI features."
        )

    return st.session_state.page