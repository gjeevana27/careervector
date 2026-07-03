import streamlit as st
from src.services.groq.interview_service import InterviewService


def build_transcript(messages: list) -> str:
    lines = []
    for m in messages:
        role = "Interviewer" if m["role"] == "assistant" else "Candidate"
        lines.append(f"{role}: {m['content']}")
    return "\n\n".join(lines)


def render_interview_prep():

    st.title("🎤 Interview Launchpad")
    st.write(
        "Practice a real interview with Alex, your AI interviewer. "
        "Questions are tailored to your resume and the specific job — "
        "get scored and coached at the end."
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
    # Job selection
    # ------------------------------------------------
    job_matches = st.session_state.get("job_matches", [])

    if not job_matches:
        st.warning(
            "No career matches found. "
            "Go to **Career Matches** first to load job matches."
        )
        return

    # ------------------------------------------------
    # Interview state init
    # ------------------------------------------------
    if "interview_active" not in st.session_state:
        st.session_state["interview_active"] = False
    if "interview_messages" not in st.session_state:
        st.session_state["interview_messages"] = []
    if "interview_complete" not in st.session_state:
        st.session_state["interview_complete"] = False
    if "interview_feedback" not in st.session_state:
        st.session_state["interview_feedback"] = None
    if "interview_job" not in st.session_state:
        st.session_state["interview_job"] = None
    if "interview_system_prompt" not in st.session_state:
        st.session_state["interview_system_prompt"] = None

    # ------------------------------------------------
    # Setup screen
    # ------------------------------------------------
    if not st.session_state["interview_active"] and \
       not st.session_state["interview_complete"]:

        st.subheader("Choose Your Interview")

        job_options = {
            f"{m['title']} @ {m['company']} "
            f"({m['score']}% match)": m
            for m in job_matches
        }

        selected_label = st.selectbox(
            "Select a job to interview for",
            options=list(job_options.keys())
        )

        selected_job = job_options[selected_label]

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {selected_job['title']}")
                st.write(
                    f"**{selected_job['company']}** • "
                    f"{selected_job.get('location', '')}"
                )
            with col2:
                st.metric(
                    "Match",
                    f"{selected_job['score']}%"
                )

        st.divider()

        st.markdown("### What to expect")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(
                "🎯 **Tailored Questions**\n\n"
                "Alex asks questions based on your "
                "actual resume AND this specific JD"
            )

        with col2:
            st.info(
                "💬 **Real Conversation**\n\n"
                "Natural back-and-forth — follow-up "
                "questions if your answers need "
                "more depth"
            )

        with col3:
            st.info(
                "📊 **Full Feedback Report**\n\n"
                "Score per answer, better answer "
                "suggestions, and next steps "
                "after the interview ends"
            )

        st.divider()

        if st.button(
            "🎤 Start Interview",
            type="primary",
            use_container_width=True
        ):
            service = InterviewService()
            system_prompt = service.get_system_prompt(
                resume_text=resume_text,
                jd_text=selected_job.get("full_description", ""),
                job_title=selected_job.get("title", ""),
                company=selected_job.get("company", "")
            )

            with st.spinner("Alex is preparing your interview..."):
                try:
                    opening = service.chat(
                        messages=[],
                        system_prompt=system_prompt
                    )
                except Exception as e:
                    error_msg = str(e)
                    if "rate_limit_exceeded" in error_msg \
                       or "429" in error_msg:
                        st.error(
                            "⏳ Groq daily token limit reached. "
                            "Please try again tomorrow or upgrade at "
                            "console.groq.com/settings/billing"
                        )
                    else:
                        st.error(f"Error starting interview: {error_msg}")
                    return

            st.session_state["interview_active"] = True
            st.session_state["interview_complete"] = False
            st.session_state["interview_feedback"] = None
            st.session_state["interview_messages"] = [
                {"role": "assistant", "content": opening}
            ]
            st.session_state["interview_job"] = selected_job
            st.session_state["interview_system_prompt"] = system_prompt
            st.rerun()

    # ------------------------------------------------
    # Active interview — chat interface
    # ------------------------------------------------
    elif st.session_state["interview_active"] and \
         not st.session_state["interview_complete"]:

        job = st.session_state["interview_job"]
        messages = st.session_state["interview_messages"]

        # Header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"**Interviewing for:** {job['title']} "
                f"@ {job['company']}"
            )
        with col2:
            if st.button("🛑 End Interview", type="secondary"):
                st.session_state["interview_active"] = False
                st.session_state["interview_complete"] = True
                st.rerun()

        st.divider()

        # Display chat history
        for message in messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="🎤"):
                    content = message["content"].replace(
                        "[INTERVIEW_COMPLETE]", ""
                    ).strip()
                    st.write(content)
            else:
                with st.chat_message("user", avatar="👤"):
                    st.write(message["content"])

        # Check if interview complete signal received
        if messages and "[INTERVIEW_COMPLETE]" in \
           messages[-1].get("content", ""):
            st.success(
                "✅ Alex has completed the interview. "
                "Click below to get your feedback report."
            )
            if st.button(
                "📊 Get My Feedback Report",
                type="primary",
                use_container_width=True
            ):
                st.session_state["interview_active"] = False
                st.session_state["interview_complete"] = True
                st.rerun()
            return

        # User input
        user_input = st.chat_input("Type your answer here...")

        if user_input:
            messages.append({
                "role": "user",
                "content": user_input
            })

            with st.spinner("Alex is responding..."):
                try:
                    service = InterviewService()
                    response = service.chat(
                        messages=messages,
                        system_prompt=st.session_state[
                            "interview_system_prompt"
                        ]
                    )
                except Exception as e:
                    error_msg = str(e)
                    if "rate_limit_exceeded" in error_msg \
                       or "429" in error_msg:
                        st.error(
                            "⏳ Groq token limit reached. "
                            "Click **End Interview** to save your "
                            "progress and get feedback tomorrow."
                        )
                        st.session_state["interview_messages"] = messages
                        return
                    else:
                        st.error(f"Error: {error_msg}")
                        return

            messages.append({
                "role": "assistant",
                "content": response
            })

            st.session_state["interview_messages"] = messages
            st.rerun()

    # ------------------------------------------------
    # Interview complete — generate + show feedback
    # ------------------------------------------------
    elif st.session_state["interview_complete"]:

        messages = st.session_state.get("interview_messages", [])
        job = st.session_state.get("interview_job", {})

        # Generate feedback if not already done
        if not st.session_state["interview_feedback"]:
            with st.spinner(
                "Analyzing your interview performance..."
            ):
                try:
                    transcript = build_transcript(messages)
                    service = InterviewService()
                    feedback = service.generate_feedback(
                        transcript=transcript,
                        resume_text=resume_text,
                        jd_text=job.get("full_description", ""),
                        job_title=job.get("title", ""),
                        company=job.get("company", "")
                    )
                    st.session_state["interview_feedback"] = feedback
                    st.rerun()

                except Exception as e:
                    error_msg = str(e)
                    if "rate_limit_exceeded" in error_msg \
                       or "429" in error_msg:
                        st.error(
                            "⏳ Groq daily token limit reached. "
                            "This resets every 24 hours. "
                            "Please try again tomorrow or upgrade at "
                            "console.groq.com/settings/billing"
                        )
                        st.info(
                            "Your interview transcript is saved below. "
                            "Come back tomorrow to generate your "
                            "feedback report."
                        )
                        with st.expander("📄 View Your Transcript"):
                            st.text(build_transcript(messages))

                        if st.button(
                            "🔄 Start New Interview",
                            use_container_width=True
                        ):
                            st.session_state["interview_active"] = False
                            st.session_state["interview_complete"] = False
                            st.session_state["interview_messages"] = []
                            st.session_state["interview_feedback"] = None
                            st.session_state["interview_job"] = None
                            st.rerun()
                    else:
                        st.error(f"Error: {error_msg}")
                    return

        feedback = st.session_state["interview_feedback"]

        # ------------------------------------------------
        # Feedback report
        # ------------------------------------------------
        st.subheader("📊 Interview Performance Report")
        st.write(
            f"**Role:** {job.get('title', '')} "
            f"@ {job.get('company', '')}"
        )

        st.divider()

        # Overall score + recommendation
        overall = int(feedback.get("overall_score", 0))
        recommendation = feedback.get("hiring_recommendation", "")
        summary = feedback.get("overall_summary", "")

        col1, col2 = st.columns([1, 2])

        with col1:
            if overall >= 80:
                st.success(f"### 🏆 {overall}/100")
            elif overall >= 60:
                st.warning(f"### 📊 {overall}/100")
            else:
                st.error(f"### 📉 {overall}/100")

            st.metric("Overall Score", f"{overall}/100")

            if recommendation == "Strong Yes":
                st.success(f"✅ {recommendation}")
            elif recommendation == "Yes":
                st.success(f"👍 {recommendation}")
            elif recommendation == "Maybe":
                st.warning(f"🤔 {recommendation}")
            else:
                st.error(f"❌ {recommendation}")

        with col2:
            if summary:
                st.info(f"**Summary:** {summary}")

            best = feedback.get("best_answer", "")
            if best:
                st.success(f"🏆 **Best Answer:** {best}")

            weakest = feedback.get("weakest_answer", "")
            if weakest:
                st.error(f"⚠️ **Weakest Answer:** {weakest}")

        st.divider()

        # ------------------------------------------------
        # Answer by answer evaluation
        # ------------------------------------------------
        evaluations = feedback.get("answer_evaluations", [])

        if evaluations:
            st.subheader("📝 Answer-by-Answer Breakdown")

            for i, eval_item in enumerate(evaluations):
                score = int(eval_item.get("score", 0))

                if score >= 8:
                    color = "🟢"
                elif score >= 5:
                    color = "🟡"
                else:
                    color = "🔴"

                question_preview = eval_item.get(
                    "question", ""
                )[:80]

                with st.expander(
                    f"{color} Q{i+1}: {question_preview}... "
                    f"— Score: {score}/10"
                ):
                    st.markdown(
                        f"**Question:** "
                        f"{eval_item.get('question', '')}"
                    )

                    st.divider()

                    st.markdown("**Your Answer:**")
                    st.write(eval_item.get("answer_given", ""))

                    st.divider()

                    e_col1, e_col2 = st.columns(2)

                    with e_col1:
                        good = eval_item.get("what_was_good", "")
                        if good:
                            st.success(
                                f"✅ **What was good:**\n{good}"
                            )

                    with e_col2:
                        weak = eval_item.get("what_was_weak", "")
                        if weak:
                            st.error(
                                f"❌ **What was weak:**\n{weak}"
                            )

                    better = eval_item.get("better_answer", "")
                    if better:
                        st.info(
                            f"💡 **Stronger Answer:**\n\n{better}"
                        )

        st.divider()

        # ------------------------------------------------
        # Strengths + Areas to improve
        # ------------------------------------------------
        s_col, a_col = st.columns(2)

        with s_col:
            st.subheader("💚 Strengths")
            for strength in feedback.get("strengths", []):
                st.success(f"✅ {strength}")

        with a_col:
            st.subheader("🔧 Areas to Improve")
            for area in feedback.get("areas_to_improve", []):
                st.warning(f"⚠️ {area}")

        st.divider()

        # ------------------------------------------------
        # Skills demonstrated vs not
        # ------------------------------------------------
        sk_col1, sk_col2 = st.columns(2)

        with sk_col1:
            st.subheader("✅ Skills Demonstrated")
            for skill in feedback.get(
                "skills_demonstrated", []
            ):
                st.success(f"• {skill}")

        with sk_col2:
            st.subheader("❌ Skills Not Shown")
            for skill in feedback.get(
                "skills_not_demonstrated", []
            ):
                st.error(f"• {skill}")

        st.divider()

        # ------------------------------------------------
        # Next steps
        # ------------------------------------------------
        next_steps = feedback.get("next_steps", [])

        if next_steps:
            st.subheader(
                "🚀 Next Steps Before Your Next Interview"
            )
            for i, step in enumerate(next_steps):
                st.info(f"**{i+1}.** {step}")

        st.divider()

        # ------------------------------------------------
        # Transcript + restart
        # ------------------------------------------------
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🔄 Start New Interview",
                use_container_width=True,
                type="primary"
            ):
                st.session_state["interview_active"] = False
                st.session_state["interview_complete"] = False
                st.session_state["interview_messages"] = []
                st.session_state["interview_feedback"] = None
                st.session_state["interview_job"] = None
                st.session_state["interview_system_prompt"] = None
                st.rerun()

        with col2:
            with st.expander("📄 View Full Transcript"):
                transcript = build_transcript(messages)
                st.text(transcript)