import streamlit as st


def render_hero():

    with st.container(border=True):

        st.markdown(
            """
            <h1 style="
                color:#DC2626;
                font-size:42px;
                font-weight:800;
                margin-bottom:0;
            ">
                Every Great Career Needs a Vector
            </h1>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <h2 style="
                color:#111827;
                margin-top:0;
            ">
                Upload your resume and let's discover yours
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            "Analyze your resume, discover matching jobs, identify skill gaps, "
            "improve your ATS score, and prepare for interviews with AI-powered insights."
        )

        # -----------------------------
        # Upload Button
        # -----------------------------

        if st.button(
            "Upload Resume",
            type="primary",
            key="hero_upload",
        ):

            st.session_state.page = "Vector Analysis"
            st.rerun()

        st.caption(
            "Your resume stays private. Your potential doesn't."
        )