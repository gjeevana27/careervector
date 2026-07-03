import streamlit as st


def render_projects(projects):

    st.header("Projects")

    if not projects:
        st.info("No projects found.")
        return

    for project in projects:

        with st.container(border=True):

            # Title — matches prompt key exactly
            title = (
                project.get("title")
                or project.get("project_name")
                or project.get("name")
                or "Untitled Project"
            )

            st.subheader(title)

            # Technologies — prompt returns a list
            technologies = project.get("technologies") or []

            if isinstance(technologies, str):
                technologies = [t.strip() for t in technologies.split(",")]

            if technologies:
                st.write("**Technologies:** " + ", ".join(technologies))

            # Description
            description = project.get("description") or ""
            if description:
                st.write(description)

            # Achievements / bullet points
            achievements = project.get("achievements") or []

            if isinstance(achievements, str):
                achievements = [achievements]

            for achievement in achievements:
                if achievement.strip():
                    st.markdown(f"- {achievement}")

        st.write("")