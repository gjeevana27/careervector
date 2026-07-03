from pathlib import Path
import streamlit as st


def load_theme(page_title="CareerVector"):

    st.set_page_config(
        page_title=page_title,
        page_icon="assets/images/logo_cv.svg",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    css_path = Path("assets/css/styles.css")

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <style>
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )