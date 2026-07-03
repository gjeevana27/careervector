import streamlit as st
from src.matching.matcher import JobMatcher
from src.services.groq.career_service import CareerService


def clean(value):
    """Convert nan/None to empty string."""
    if not value or str(value).lower() == "nan":
        return ""
    return str(value)


def render_job_matches():

    st.title("Career Matches")
    st.write(
        "Discover opportunities tailored to your skills, "
        "experience, and career aspirations."
    )
    st.divider()

    # ------------------------------------------------
    # Check resume is uploaded
    # ------------------------------------------------
    if "resume" not in st.session_state or \
       "resume_text" not in st.session_state:
        st.warning(
            "No resume found. Please go to **Vector Analysis** "
            "and upload your resume first."
        )
        return

    resume_text = st.session_state["resume_text"]
    resume = st.session_state.get("resume", None)

    # ------------------------------------------------
    # Search & Filters
    # ------------------------------------------------
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        search_query = st.text_input(
            "Search Jobs",
            placeholder="Machine Learning Engineer",
        )

    with col2:
        location_filter = st.selectbox(
            "Location",
            ["Anywhere", "Remote", "United States",
             "New York", "California", "Texas", "Virginia"],
        )

    with col3:
        experience_filter = st.selectbox(
            "Experience",
            ["All", "Internship", "Entry Level",
             "Mid Level", "Senior"],
        )

    st.divider()

    # ------------------------------------------------
    # Load matches from Pinecone
    # ------------------------------------------------
    if "job_matches" not in st.session_state:
        with st.spinner("Finding best matches from Pinecone..."):
            try:
                matcher = JobMatcher()
                matches = matcher.match(
                    resume_text=resume_text,
                    top_k=15,
                    resume=resume
                )
                st.session_state["job_matches"] = matches
            except Exception as e:
                st.error(f"Matching error: {str(e)}")
                return

    matches = st.session_state["job_matches"]

    # ------------------------------------------------
    # Apply filters
    # ------------------------------------------------
    filtered = matches

    if search_query.strip():
        filtered = [
            m for m in filtered
            if search_query.lower() in m["title"].lower()
            or search_query.lower() in m["company"].lower()
        ]

    if location_filter != "Anywhere":
        if location_filter == "Remote":
            filtered = [
                m for m in filtered
                if m.get("is_remote") is True
                or "remote" in clean(m["location"]).lower()
            ]
        else:
            filtered = [
                m for m in filtered
                if location_filter.lower() in
                clean(m["location"]).lower()
            ]

    if experience_filter != "All":
        filtered = [
            m for m in filtered
            if experience_filter.lower() in m["title"].lower()
            or experience_filter.lower() in
            clean(m.get("employment_type", "")).lower()
        ]

    # ------------------------------------------------
    # Results header
    # ------------------------------------------------
    st.subheader(
        f"Recommended Opportunities ({len(filtered)} matches)"
    )

    if not filtered:
        st.info("No matches found for your current filters.")
        if st.button("Clear Filters"):
            st.rerun()
        return

    if "gap_results" not in st.session_state:
        st.session_state["gap_results"] = {}

    # ------------------------------------------------
    # Job cards
    # ------------------------------------------------
    for i, job in enumerate(filtered):

        score = job["score"]
        title = clean(job["title"]) or "Untitled Role"
        company = clean(job["company"]) or "Unknown Company"
        location = clean(job["location"])
        skills = clean(job.get("required_skills", ""))
        emp_type = clean(job.get("employment_type", ""))
        apply_link = clean(job.get("apply_link", ""))
        is_remote = job.get("is_remote", False)

        if score >= 70:
            icon = "🟢"
        elif score >= 50:
            icon = "🟡"
        else:
            icon = "🔴"

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"### {title}")
                remote_tag = " 🌐 Remote" if is_remote else ""
                location_display = (
                    f"{location}{remote_tag}"
                    if location else remote_tag
                )
                st.write(
                    f"**{company}**" +
                    (f" • {location_display}"
                     if location_display else "")
                )
                if emp_type:
                    st.caption(f"📋 {emp_type}")
                if skills:
                    st.caption(f"🛠 Skills: {skills[:200]}")

            with col2:
                st.metric("Match", f"{score}%")
                st.write(icon)

            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                if apply_link:
                    st.link_button(
                        "Apply Now →",
                        apply_link,
                        use_container_width=True
                    )

            with btn_col2:
                details_clicked = st.button(
                    "View Details",
                    key=f"details_{i}",
                    use_container_width=True
                )

            if details_clicked:
                gap_key = f"gap_{job['jd_id']}"
                show_key = f"show_{job['jd_id']}"

                if gap_key not in st.session_state["gap_results"]:
                    with st.spinner(
                        "Running gap analysis with Groq..."
                    ):
                        try:
                            service = CareerService()
                            gap = service.gap_analysis(
                                resume_text=resume_text,
                                jd_text=job["full_description"],
                                job_title=title
                            )
                            st.session_state[
                                "gap_results"
                            ][gap_key] = gap
                        except Exception as e:
                            st.error(f"Analysis error: {str(e)}")

                st.session_state[show_key] = not st.session_state.get(
                    show_key, False
                )

            show_key = f"show_{job['jd_id']}"
            gap_key = f"gap_{job['jd_id']}"

            if st.session_state.get(show_key) and \
               gap_key in st.session_state["gap_results"]:

                gap = st.session_state["gap_results"][gap_key]

                st.divider()

                with st.expander("📄 Full Job Description"):
                    st.write(job["full_description"])

                fit = gap.get("overall_fit", "Unknown")
                if fit == "Strong":
                    st.success(f"✅ Overall Fit: {fit}")
                elif fit == "Moderate":
                    st.warning(f"⚠️ Overall Fit: {fit}")
                else:
                    st.error(f"❌ Overall Fit: {fit}")

                st.write(
                    f"**Summary:** "
                    f"{gap.get('match_summary', '')}"
                )

                st.divider()

                g1, g2 = st.columns(2)

                with g1:
                    st.success("✅ You already have these")
                    for skill in gap.get("matching_skills", []):
                        st.markdown(f"- {skill}")

                with g2:
                    st.error("❌ You are missing these")
                    for skill in gap.get("missing_skills", []):
                        st.markdown(f"- {skill}")

                keywords = gap.get("keywords_to_add", [])
                if keywords:
                    st.warning(
                        "🔑 **Keywords to add:** " +
                        " · ".join(keywords)
                    )

                bullet = gap.get("suggested_bullet", "")
                if bullet:
                    st.info(
                        f"✍️ **Suggested Resume Bullet:**"
                        f"\n\n> {bullet}"
                    )

                points = gap.get("interview_talking_points", [])
                if points:
                    st.markdown("**🎤 Interview Talking Points:**")
                    for point in points:
                        st.markdown(f"- {point}")

        st.write("")

    # ------------------------------------------------
    # Bottom bar
    # ------------------------------------------------
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Refresh Matches",
            use_container_width=True
        ):
            if "job_matches" in st.session_state:
                del st.session_state["job_matches"]
            if "gap_results" in st.session_state:
                del st.session_state["gap_results"]
            st.rerun()

    with col2:
        st.caption(
            f"Showing {len(filtered)} of "
            f"{len(matches)} total matches"
        )