import streamlit as st

from src.ui.components.feature_cards import feature_card


def render_dashboard():

    st.header("Dashboard")

    st.write(
        "Everything you need to accelerate your career, all in one place."
    )

    st.write("")

    # ----------------------------
    # Row 1
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            title="Resume Analysis",
            description="Every resume tells a story. Let's uncover yours.",
            button_text="Open",
            page="Vector Analysis",
        )

    with col2:

        feature_card(
            title="Career Matches",
            description="Find opportunities tailored to your skills and career goals.",
            button_text="Explore",
            page="Career Matches",
        )

    with col3:

        feature_card(
            title="ATS Radar",
            description="See how recruiter-friendly your resume really is.",
            button_text="Check",
            page="ATS Radar",
        )

    st.write("")

    # ----------------------------
    # Row 2
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            title="Growth Path",
            description="Discover the skills that will move your career forward.",
            button_text="Discover",
            page="Growth Path",
        )

    with col2:

        feature_card(
            title="Vector Boost",
            description="Transform your resume with personalized AI suggestions.",
            button_text="Optimize",
            page="Vector Boost",
        )

    with col3:

        feature_card(
            title="Interview Launchpad",
            description="Practice smarter with AI-generated interview questions.",
            button_text="Practice",
            page="Interview Launchpad",
        )