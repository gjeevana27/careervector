import streamlit as st
from src.services.groq.optimizer_service import OptimizerService


def render_resume_optimizer():

    st.title("⚡ Vector Boost")
    st.write(
        "Enhance your resume with AI-powered rewrites "
        "tailored specifically to your target job — "
        "stronger bullets, better tone, and JD-matched language."
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
    # Job selection from Career Matches
    # ------------------------------------------------
    job_matches = st.session_state.get("job_matches", [])

    if not job_matches:
        st.warning(
            "No career matches found. "
            "Go to **Career Matches** first to load job matches."
        )
        return

    st.subheader("Select Target Job")

    job_options = {
        f"{m['title']} @ {m['company']} ({m['score']}% match)": m
        for m in job_matches
    }

    selected_label = st.selectbox(
        "Choose the job you want to optimize your resume for",
        options=list(job_options.keys())
    )

    selected_job = job_options[selected_label]
    jd_text = selected_job.get("full_description", "")
    job_title = selected_job.get("title", "")
    company = selected_job.get("company", "")
    match_score = selected_job.get("score", 0)

    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {job_title}")
            st.write(
                f"**{company}** • "
                f"{selected_job.get('location', '')}"
            )
        with col2:
            st.metric("Current Match", f"{match_score}%")

    st.divider()

    # ------------------------------------------------
    # Run optimization
    # ------------------------------------------------
    if st.button(
        "⚡ Boost My Resume",
        type="primary",
        use_container_width=True
    ):
        with st.spinner(
            f"Optimizing your resume for {job_title}..."
        ):
            try:
                service = OptimizerService()
                result = service.optimize(
                    resume_text=resume_text,
                    jd_text=jd_text,
                    job_title=job_title,
                    company=company
                )
                st.session_state["optimizer"] = result
                st.success("Resume boost complete!")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                return

    # ------------------------------------------------
    # Show results
    # ------------------------------------------------
    if "optimizer" not in st.session_state:
        st.info(
            "Select a job and click **Boost My Resume** "
            "to get AI-powered rewrites."
        )
        return

    result = st.session_state["optimizer"]

    # ------------------------------------------------
    # Boost score
    # ------------------------------------------------
    before = int(result.get("overall_boost_score", 0))
    after = int(result.get("estimated_score_after", 0))
    summary = result.get("boost_summary", "")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Writing Strength Before", f"{before}/100")
        st.progress(before / 100)

    with col2:
        st.metric(
            "Writing Strength After",
            f"{after}/100",
            delta=f"+{after - before}"
        )
        st.progress(after / 100)

    with col3:
        improvement = after - before
        if improvement >= 20:
            st.success(f"🚀 +{improvement} point improvement")
        elif improvement >= 10:
            st.warning(f"📈 +{improvement} point improvement")
        else:
            st.info(f"📊 +{improvement} point improvement")

    if summary:
        st.info(f"**Summary:** {summary}")

    st.divider()

    # ------------------------------------------------
    # Headline options
    # ------------------------------------------------
    headlines = result.get("headline_options", [])

    if headlines:
        st.subheader("✍️ Professional Headline Options")
        st.write(
            "Replace your current headline with one "
            "of these tailored versions:"
        )

        for i, headline in enumerate(headlines):
            with st.container(border=True):
                st.write(f"**Option {i+1}:** {headline}")

    st.divider()

    # ------------------------------------------------
    # Summary rewrite — before/after
    # ------------------------------------------------
    summary_rewrite = result.get("summary_rewrite", {})

    if summary_rewrite:
        st.subheader("📝 Summary Rewrite")

        s_col1, s_col2 = st.columns(2)

        with s_col1:
            st.markdown("**❌ Original**")
            with st.container(border=True):
                st.write(
                    summary_rewrite.get("original", "")
                    or "No original summary found."
                )

        with s_col2:
            st.markdown("**✅ Rewritten**")
            with st.container(border=True):
                st.success(
                    summary_rewrite.get("rewritten", "")
                    or "No rewrite generated."
                )

        improvements = summary_rewrite.get("improvements_made", [])
        if improvements:
            st.caption(
                "**Improvements:** " +
                " · ".join(improvements)
            )

    st.divider()

    # ------------------------------------------------
    # Bullet rewrites — before/after
    # ------------------------------------------------
    bullet_rewrites = result.get("bullet_rewrites", [])

    if bullet_rewrites:
        st.subheader("🎯 Bullet Point Rewrites")
        st.write(
            "Your weakest bullets rewritten in STAR format, "
            "tailored to this role:"
        )

        for i, bullet in enumerate(bullet_rewrites):
            with st.container(border=True):

                st.caption(f"Bullet {i + 1}")

                b_col1, b_col2 = st.columns(2)

                with b_col1:
                    st.markdown("**❌ Original**")
                    st.write(bullet.get("original", ""))

                with b_col2:
                    st.markdown("**✅ Rewritten**")
                    st.success(bullet.get("rewritten", ""))

                why = bullet.get("why", "")
                if why:
                    st.caption(f"💡 {why}")

            st.write("")

    st.divider()

    # ------------------------------------------------
    # Weak verbs
    # ------------------------------------------------
    weak_verbs = result.get("weak_verbs_found", [])

    if weak_verbs:
        st.subheader("💪 Power Word Upgrades")
        st.write(
            "Replace these weak verbs with stronger alternatives:"
        )

        cols = st.columns(3)

        for i, verb in enumerate(weak_verbs):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(
                        f"~~{verb.get('original_verb', '')}~~ "
                        f"→ **{verb.get('stronger_verb', '')}**"
                    )
                    example = verb.get("example_bullet", "")
                    if example:
                        st.caption(f"e.g. {example}")

    st.divider()

    # ------------------------------------------------
    # JD language to mirror
    # ------------------------------------------------
    jd_language = result.get("jd_language_to_mirror", [])

    if jd_language:
        st.subheader("🪞 Mirror the JD Language")
        st.write(
            "Use these exact phrases from the job description "
            "naturally in your resume:"
        )

        for item in jd_language:
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.info(
                        f"**JD says:** "
                        f"\"{item.get('jd_phrase', '')}\""
                    )
                with col2:
                    st.write(
                        f"**How to use:** "
                        f"{item.get('how_to_use', '')}"
                    )

    st.divider()

    # ------------------------------------------------
    # Tone analysis
    # ------------------------------------------------
    tone = result.get("tone_analysis", {})

    if tone:
        st.subheader("🎭 Tone Analysis")

        t_col1, t_col2 = st.columns(2)

        with t_col1:
            current = tone.get("current_tone", "")
            if current:
                st.warning(f"**Current Tone:** {current}")

        with t_col2:
            recommended = tone.get("recommended_tone", "")
            if recommended:
                st.success(f"**Recommended Tone:** {recommended}")

        tips = tone.get("tone_tips", [])
        if tips:
            st.write("**Tips:**")
            for tip in tips:
                st.caption(f"• {tip}")

    st.divider()

    # ------------------------------------------------
    # Skills to highlight
    # ------------------------------------------------
    skills_highlight = result.get("skills_to_highlight", [])

    if skills_highlight:
        st.subheader("🌟 Skills to Emphasize")
        st.write(
            "These skills from your resume need more visibility "
            "for this role:"
        )

        for skill in skills_highlight:
            with st.container(border=True):
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.success(f"**{skill.get('skill', '')}**")
                with col2:
                    st.write(skill.get("reason", ""))
                    where = skill.get("where_to_add", "")
                    if where:
                        st.caption(f"📍 Add to: {where}")

    st.divider()

    # ------------------------------------------------
    # Re-run button
    # ------------------------------------------------
    if st.button(
        "🔄 Boost for Different Job",
        use_container_width=True
    ):
        if "optimizer" in st.session_state:
            del st.session_state["optimizer"]
        st.rerun()