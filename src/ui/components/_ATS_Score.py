import streamlit as st
from src.services.groq.ats_service import ATSService


def score_color(score: int) -> str:
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    else:
        return "🔴"


def render_score_bar(label: str, score: int):
    icon = score_color(score)
    st.write(f"**{label}** {icon}")
    st.progress(int(score) / 100)
    st.caption(f"{score}/100")
    st.write("")


def render_ats_score():

    st.title("🎯 ATS Radar")
    st.write(
        "Analyze how well your resume performs against "
        "Applicant Tracking Systems — both generally "
        "and for a specific job."
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

    # ------------------------------------------------
    # Mode selection
    # ------------------------------------------------
    st.subheader("Analysis Mode")

    mode = st.radio(
        "Choose how to analyze your resume",
        [
            "General ATS Check",
            "Score against a Career Match",
            "Paste a Job Description"
        ],
        horizontal=True
    )

    jd_text = ""
    job_title = ""

    # ------------------------------------------------
    # Career match selection
    # ------------------------------------------------
    if mode == "Score against a Career Match":

        job_matches = st.session_state.get("job_matches", [])

        if not job_matches:
            st.warning(
                "No career matches found. "
                "Go to **Career Matches** first to load jobs."
            )
            return

        job_options = {
            f"{m['title']} @ {m['company']} "
            f"({m['score']}% match)": m
            for m in job_matches
        }

        selected_label = st.selectbox(
            "Choose a job from your matches",
            options=list(job_options.keys())
        )

        selected_job = job_options[selected_label]
        jd_text = selected_job.get("full_description", "")
        job_title = selected_job.get("title", "")

        st.success(
            f"Analyzing against: **{job_title}** "
            f"@ {selected_job.get('company', '')}"
        )

    # ------------------------------------------------
    # Manual JD paste
    # ------------------------------------------------
    elif mode == "Paste a Job Description":

        job_title = st.text_input(
            "Job Title",
            placeholder="Data Engineer"
        )

        jd_text = st.text_area(
            "Paste Job Description",
            placeholder="Paste the full job description here...",
            height=200
        )

    st.divider()

    # ------------------------------------------------
    # Run analysis
    # ------------------------------------------------
    if st.button(
        "🔍 Run ATS Analysis",
        type="primary",
        use_container_width=True
    ):
        with st.spinner("Scanning resume with ATS analyzer..."):
            try:
                ats = ATSService().analyze(
                    resume_text=resume_text,
                    jd_text=jd_text,
                    job_title=job_title
                )
                st.session_state["ats"] = ats
                st.success("ATS analysis complete!")

            except Exception as e:
                st.error(str(e))
                return

    # ------------------------------------------------
    # Show results
    # ------------------------------------------------
    if "ats" not in st.session_state:
        st.info("Click **Run ATS Analysis** to get your score.")
        return

    ats = st.session_state["ats"]
    overall = int(ats.get("overall_score", 0))

    st.divider()

    # Big overall score
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"<h1 style='text-align:center; font-size:72px;'>"
            f"{score_color(overall)}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h1 style='text-align:center;'>{overall}/100</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center; font-size:18px;'>"
            "Overall ATS Score</p>",
            unsafe_allow_html=True
        )

    st.divider()

    # ------------------------------------------------
    # Top 3 scores
    # ------------------------------------------------
    st.subheader("📊 Score Breakdown")

    c1, c2, c3 = st.columns(3)

    with c1:
        fmt = int(ats.get("format_score", 0))
        st.metric("Format", f"{fmt}/100", score_color(fmt))
        st.progress(fmt / 100)

    with c2:
        kw = int(ats.get("keyword_score", 0))
        st.metric("Keywords", f"{kw}/100", score_color(kw))
        st.progress(kw / 100)

    with c3:
        sec = int(ats.get("section_score", 0))
        st.metric("Sections", f"{sec}/100", score_color(sec))
        st.progress(sec / 100)

    st.divider()

    # ------------------------------------------------
    # Section breakdown
    # ------------------------------------------------
    section_breakdown = ats.get("section_breakdown", {})

    if section_breakdown:
        st.subheader("📋 Section Scores")

        col1, col2 = st.columns(2)
        items = list(section_breakdown.items())
        half = len(items) // 2

        with col1:
            for key, score in items[:half]:
                render_score_bar(
                    key.replace("_", " ").title(),
                    int(score)
                )

        with col2:
            for key, score in items[half:]:
                render_score_bar(
                    key.replace("_", " ").title(),
                    int(score)
                )

    st.divider()

    # ------------------------------------------------
    # Keywords
    # ------------------------------------------------
    st.subheader("🔑 Keyword Analysis")

    kw_col1, kw_col2 = st.columns(2)

    with kw_col1:
        matched = ats.get("matched_keywords", [])
        if matched:
            st.success(f"✅ Matched ({len(matched)})")
            for kw in matched:
                st.markdown(f"- {kw}")

    with kw_col2:
        missing = ats.get("missing_keywords", [])
        if missing:
            st.error(f"❌ Missing ({len(missing)})")
            for kw in missing:
                st.markdown(f"- {kw}")

    st.divider()

    # ------------------------------------------------
    # Action verbs
    # ------------------------------------------------
    st.subheader("💪 Action Verbs")

    av_col1, av_col2 = st.columns(2)

    with av_col1:
        found_verbs = ats.get("action_verbs_found", [])
        if found_verbs:
            st.success("✅ Found")
            st.write(", ".join(found_verbs))

    with av_col2:
        suggested_verbs = ats.get("action_verbs_suggested", [])
        if suggested_verbs:
            st.warning("💡 Add These")
            st.write(", ".join(suggested_verbs))

    st.divider()

    # ------------------------------------------------
    # Quantification
    # ------------------------------------------------
    st.subheader("📈 Quantification")

    q_col1, q_col2 = st.columns(2)

    with q_col1:
        quant_found = ats.get("quantification_examples", [])
        if quant_found:
            st.success("✅ Quantified Achievements")
            for q in quant_found:
                st.markdown(f"- {q}")

    with q_col2:
        quant_suggestions = ats.get("quantification_suggestions", [])
        if quant_suggestions:
            st.warning("💡 Add Metrics Here")
            for q in quant_suggestions:
                st.markdown(f"- {q}")

    st.divider()

    # ------------------------------------------------
    # Strengths + Recommendations
    # ------------------------------------------------
    s_col, r_col = st.columns(2)

    with s_col:
        st.subheader("💚 Strengths")
        for strength in ats.get("strengths", []):
            st.success(f"✅ {strength}")

    with r_col:
        st.subheader("🔧 Recommendations")
        for rec in ats.get("recommendations", []):
            st.warning(f"⚠️ {rec}")

    # Formatting issues
    fmt_issues = ats.get("formatting_issues", [])
    if fmt_issues:
        st.divider()
        st.subheader("⚠️ Formatting Issues")
        for issue in fmt_issues:
            st.error(f"- {issue}")

    st.divider()

    # Re-run button
    if st.button("🔄 Re-run Analysis", use_container_width=True):
        if "ats" in st.session_state:
            del st.session_state["ats"]
        st.rerun()