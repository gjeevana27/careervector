import streamlit as st

from src.resume.analyzer import ResumeAnalyzer

from src.ui.components.cards.candidate_header import render_candidate
from src.ui.components.cards.summary_card import render_summary
from src.ui.components.cards.skills_section import render_skills
from src.ui.components.cards.education_card import render_education
from src.ui.components.cards.experience_card import render_experience
from src.ui.components.cards.project_card import render_projects
from src.ui.components.cards.certification_card import render_certifications


def clear_all_cached_results():
    """Clear all session state that depends on resume content."""
    keys_to_clear = [
        "job_matches",
        "gap_results",
        "ats",
        "skill_gap",
        "skill_gap_job",
        "optimizer",
        "interview_active",
        "interview_messages",
        "interview_complete",
        "interview_feedback",
        "interview_job",
        "interview_system_prompt",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def render_resume_analysis():

    st.title("Resume Analysis")

    st.write(
        "Upload your resume and let CareerVector uncover strengths, "
        "identify opportunities, and help you build a resume that stands out."
    )

    st.divider()

    # ----------------------------------------------------
    # Upload Section
    # ----------------------------------------------------

    st.subheader("Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
    )

    if uploaded_file is None:

        st.info(
            """
📄 Ready to get started?

Upload your resume and CareerVector will analyze:

- Resume Structure

- Skills & Technologies

- Education

- Experience

- Projects

- Certifications
"""
        )

    else:

        st.success(
            f"Resume Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "Analyze Resume",
            type="primary",
            use_container_width=True,
        ):

            try:

                with st.spinner(
                    "Analyzing your resume..."
                ):

                    analyzer = ResumeAnalyzer()

                    resume, resume_text = analyzer.analyze(
                        uploaded_file
                    )

                    # Clear all cached results from previous resume
                    clear_all_cached_results()

                    st.session_state["resume"] = resume
                    st.session_state["resume_text"] = resume_text
                    st.session_state["uploaded_resume"] = uploaded_file

                st.success(
                    "Resume analyzed successfully!"
                )

            except Exception as e:

                st.error(str(e))

    # ----------------------------------------------------
    # Resume Output
    # ----------------------------------------------------

    if "resume" in st.session_state:

        resume = st.session_state["resume"]

        st.divider()

        render_candidate(
            resume["candidate"]
        )

        st.divider()

        render_summary(
            resume["summary"]
        )

        st.divider()

        render_skills(
            resume["skills"]
        )

        st.divider()

        render_education(
            resume["education"]
        )

        st.divider()

        render_experience(
            resume["experience"]
        )

        st.divider()

        render_projects(
            resume["projects"]
        )

        st.divider()

        render_certifications(
            resume["certifications"]
        )

    # ----------------------------------------------------
    # Status
    # ----------------------------------------------------

    st.divider()

    st.subheader("Analysis Status")

    if "resume" in st.session_state:

        st.success(
            "Resume analyzed successfully and stored "
            "for all CareerVector modules."
        )

    else:

        st.info(
            "No resume analyzed yet."
        )