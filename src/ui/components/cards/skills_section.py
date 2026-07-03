import streamlit as st


def render_skills(skills):

    st.header("Skills")

    if not skills:
        st.info("No skills detected.")
        return

    # Handle if Groq returns skills as a single string
    # e.g. "Python, SQL, Docker" instead of a list
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",")]

    # Filter out any empty strings
    skills = [s for s in skills if s.strip()]

    if not skills:
        st.info("No skills detected.")
        return

    cols = st.columns(4)

    for i, skill in enumerate(skills):
        cols[i % 4].success(skill)