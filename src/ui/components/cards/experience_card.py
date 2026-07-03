import streamlit as st


def render_experience(experience):

    st.header("Experience")

    if not experience:
        st.info("No experience found.")
        return

    for exp in experience:

        with st.container(border=True):

            # Title — matches prompt key "title"
            title = (
                exp.get("title")
                or exp.get("job_title")
                or exp.get("position")
                or exp.get("role")
                or "Untitled Role"
            )

            st.subheader(title)

            # Company
            company = (
                exp.get("company")
                or exp.get("organization")
                or exp.get("employer")
                or ""
            )

            if company:
                st.write(f"**{company}**")

            # Location
            location = exp.get("location") or ""
            if location:
                st.write(f"📍 {location}")

            # Duration
            duration = (
                exp.get("duration")
                or exp.get("dates")
                or exp.get("period")
                or ""
            )

            if duration:
                st.caption(f"🗓 {duration}")

            # Achievements
            achievements = (
                exp.get("achievements")
                or exp.get("responsibilities")
                or exp.get("highlights")
                or []
            )

            if isinstance(achievements, str):
                achievements = [achievements]

            for achievement in achievements:
                if achievement.strip():
                    st.markdown(f"- {achievement}")

        st.write("")