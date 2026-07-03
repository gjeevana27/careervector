import streamlit as st
from src.ui.icon import icon


def action_card(icon_name, title, description, button_label, key):

    with st.container(border=True):

        col1, col2 = st.columns([1, 5])

        with col1:
            icon(icon_name, 28)

        with col2:
            st.markdown(f"### {title}")

        st.write(description)

        st.button(
            button_label,
            key=key,
            use_container_width=True,
        )


def render_quick_actions():

    st.markdown("## Quick Actions")
    st.caption("Choose where you'd like to begin.")

    row1 = st.columns(3)

    with row1[0]:
        action_card(
            "file-text",
            "Resume Analysis",
            "Every resume tells a story. Let's uncover yours.",
            "Open",
            "resume",
        )

    with row1[1]:
        action_card(
            "briefcase-business",
            "Job Matches",
            "Find opportunities tailored to your skills.",
            "Explore",
            "jobs",
        )

    with row1[2]:
        action_card(
            "radar",
            "ATS Score",
            "See how recruiter-friendly your resume really is.",
            "Check",
            "ats",
        )

    st.write("")

    row2 = st.columns(3)

    with row2[0]:
        action_card(
            "trending-up",
            "Skill Gap",
            "Discover what skills can move you forward.",
            "Discover",
            "skills",
        )

    with row2[1]:
        action_card(
            "sparkles",
            "Resume Optimizer",
            "Turn your resume into an interview magnet.",
            "Optimize",
            "optimizer",
        )

    with row2[2]:
        action_card(
            "mic",
            "Interview Prep",
            "Practice smarter with AI-powered questions.",
            "Practice",
            "interview",
        )