import streamlit as st
from src.services.groq.skill_service import SkillService


PRIORITY_COLOR = {
    "High": "🔴",
    "Medium": "🟡",
    "Low": "🟢"
}


def render_skill_gap():

    st.title("🚀 Growth Path")
    st.write(
        "Discover the skills that will move your career forward "
        "and unlock better opportunities — tailored to a specific job."
    )
    st.divider()

    # ------------------------------------------------
    # Check resume exists
    # ------------------------------------------------
    if "resume_text" not in st.session_state:
        st.warning(
            "No resume found. Please go to **Vector Analysis** "
            "and upload your resume first."
        )
        return

    resume_text = st.session_state["resume_text"]
    resume = st.session_state.get("resume", {})

    # ------------------------------------------------
    # Job selection from Career Matches
    # ------------------------------------------------
    job_matches = st.session_state.get("job_matches", [])

    if not job_matches:
        st.warning(
            "No career matches found. "
            "Go to **Career Matches** first to load job matches."
        )
        return

    st.subheader("Select a Job to Build Your Growth Path")

    job_options = {
        f"{m['title']} @ {m['company']} ({m['score']}% match)": m
        for m in job_matches
    }

    selected_label = st.selectbox(
        "Choose from your Career Matches",
        options=list(job_options.keys())
    )

    selected_job = job_options[selected_label]
    jd_text = selected_job.get("full_description", "")
    job_title = selected_job.get("title", "")
    company = selected_job.get("company", "")
    match_score = selected_job.get("score", 0)

    # Show selected job info
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {job_title}")
            st.write(f"**{company}** • {selected_job.get('location', '')}")
        with col2:
            st.metric("Current Match", f"{match_score}%")

    st.divider()

    # ------------------------------------------------
    # Run Analysis
    # ------------------------------------------------
    if st.button(
        "🔍 Generate Growth Path",
        type="primary",
        use_container_width=True
    ):
        with st.spinner(
            f"Building your growth path for {job_title}..."
        ):
            try:
                service = SkillService()
                result = service.analyze(
                    resume_text=resume_text,
                    jd_text=jd_text,
                    job_title=job_title,
                    company=company
                )
                st.session_state["skill_gap"] = result
                st.session_state["skill_gap_job"] = selected_label
                st.success("Growth path generated!")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                return

    # ------------------------------------------------
    # Show results
    # ------------------------------------------------
    if "skill_gap" not in st.session_state:
        st.info(
            "Select a job from your Career Matches "
            "and click **Generate Growth Path**."
        )
        return

    result = st.session_state["skill_gap"]

    # Job fit summary
    summary = result.get("job_fit_summary", "")
    if summary:
        st.info(f"**Job Fit Summary:** {summary}")

    st.divider()

    # ------------------------------------------------
    # Skills you have vs need
    # ------------------------------------------------
    st.subheader("🎯 Skills Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Skills You Already Have")
        skills_have = result.get("skills_you_have", [])
        if skills_have:
            for skill in skills_have:
                st.success(f"✅ {skill}")
        else:
            st.info("No matching skills found.")

    with col2:
        st.markdown("#### 📚 Skills to Learn")
        skills_learn = result.get("skills_to_learn", [])
        if skills_learn:
            high = [s for s in skills_learn if s.get("priority") == "High"]
            med = [s for s in skills_learn if s.get("priority") == "Medium"]
            low = [s for s in skills_learn if s.get("priority") == "Low"]

            for group, label in [(high, "High"), (med, "Medium"), (low, "Low")]:
                if group:
                    st.write(f"**{PRIORITY_COLOR.get(label, '')} {label} Priority**")
                    for s in group:
                        st.warning(f"{s.get('skill', '')}")

    st.divider()

    # ------------------------------------------------
    # Skills to learn — detailed cards
    # ------------------------------------------------
    skills_learn = result.get("skills_to_learn", [])

    if skills_learn:
        st.subheader("📚 Learning Roadmap")
        st.write("Detailed breakdown of each skill you need to learn:")

        for i, skill in enumerate(skills_learn):

            priority = skill.get("priority", "Medium")
            icon = PRIORITY_COLOR.get(priority, "🟡")

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(
                        f"### {icon} {skill.get('skill', '')}"
                    )
                    st.write(f"**Why:** {skill.get('reason', '')}")

                with col2:
                    st.metric(
                        "Time needed",
                        skill.get("estimated_time", "")
                    )
                    st.caption(f"Priority: {priority}")

                # Resources
                res_col1, res_col2 = st.columns(2)

                with res_col1:
                    free_name = skill.get("free_resource", "")
                    free_url = skill.get("free_resource_url", "")
                    if free_name and free_url:
                        st.markdown("**🆓 Free Resource:**")
                        st.markdown(f"[{free_name}]({free_url})")
                    elif free_name:
                        st.markdown(f"**🆓 Free:** {free_name}")

                with res_col2:
                    paid_name = skill.get("paid_resource", "")
                    paid_url = skill.get("paid_resource_url", "")
                    if paid_name and paid_url:
                        st.markdown("**💰 Paid Resource:**")
                        st.markdown(f"[{paid_name}]({paid_url})")
                    elif paid_name:
                        st.markdown(f"**💰 Paid:** {paid_name}")

            st.write("")

    st.divider()

    # ------------------------------------------------
    # Career trajectory
    # ------------------------------------------------
    trajectory = result.get("career_trajectory", [])

    if trajectory:
        st.subheader("📈 Career Trajectory")
        st.write(
            "Your projected career progression based on "
            "your current skills and learning path:"
        )

        cols = st.columns(len(trajectory))

        for i, stage in enumerate(trajectory):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(
                        f"**{stage.get('stage', '')}**"
                    )
                    st.write(stage.get("title", ""))

                    match_pct = stage.get("match_percentage", 0)
                    if match_pct:
                        st.metric("Match", f"{match_pct}%")
                        st.progress(int(match_pct) / 100)

                    skills_needed = stage.get(
                        "skills_needed",
                        stage.get("requirements_met", [])
                    )
                    if skills_needed:
                        for s in skills_needed[:3]:
                            st.caption(f"• {s}")

    st.divider()

    # ------------------------------------------------
    # Projects to build
    # ------------------------------------------------
    projects = result.get("projects_to_build", [])

    if projects:
        st.subheader("🛠 Projects to Build")
        st.write(
            "Build these projects to demonstrate the skills "
            "needed for this role:"
        )

        for project in projects:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### {project.get('title', '')}")
                    st.write(project.get("description", ""))

                    skills_demo = project.get("skills_demonstrated", [])
                    if skills_demo:
                        st.caption(
                            "Skills: " + " · ".join(skills_demo)
                        )

                with col2:
                    st.metric(
                        "Time",
                        project.get("estimated_time", "")
                    )

            st.write("")

    st.divider()

    # ------------------------------------------------
    # Certifications
    # ------------------------------------------------
    certs = result.get("certifications_to_get", [])

    if certs:
        st.subheader("🏆 Certifications to Get")

        for cert in certs:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(
                        f"### {cert.get('name', '')}"
                    )
                    st.write(
                        f"**Provider:** {cert.get('provider', '')}"
                    )
                    st.write(
                        f"**Why:** {cert.get('relevance', '')}"
                    )

                    cert_url = cert.get("url", "")
                    if cert_url:
                        st.markdown(f"[View Certification]({cert_url})")

                with col2:
                    cost = cert.get("cost", "")
                    if cost:
                        st.metric("Cost", cost)

            st.write("")

    st.divider()

    # ------------------------------------------------
    # Quick wins + resume gaps
    # ------------------------------------------------
    qw_col, rg_col = st.columns(2)

    with qw_col:
        st.subheader("⚡ Quick Wins")
        st.write("Do these this week:")
        quick_wins = result.get("quick_wins", [])
        if quick_wins:
            for win in quick_wins:
                st.success(f"✅ {win}")
        else:
            st.info("No quick wins identified.")

    with rg_col:
        st.subheader("🔍 Resume Gaps")
        st.write("Add these to your resume:")
        gaps = result.get("resume_gaps", [])
        if gaps:
            for gap in gaps:
                st.warning(f"⚠️ {gap}")
        else:
            st.info("No major gaps found.")

    st.divider()

    # Re-run button
    if st.button(
        "🔄 Generate for Different Job",
        use_container_width=True
    ):
        if "skill_gap" in st.session_state:
            del st.session_state["skill_gap"]
        st.rerun()