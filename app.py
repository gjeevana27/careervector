import base64
from pathlib import Path
import streamlit as st

from src.ui.theme import load_theme
from src.ui.sidebar import render_sidebar

from src.ui.components.hero import render_hero
from src.ui.components.dashboard import render_dashboard
from src.ui.components._Resume_Analysis import render_resume_analysis
from src.ui.components._Job_Matches import render_job_matches
from src.ui.components._ATS_Score import render_ats_score
from src.ui.components._Skill_Gap import render_skill_gap
from src.ui.components._Resume_Optimizer import render_resume_optimizer
from src.ui.components._Interview_Prep import render_interview_prep


def render_topbar():
    """Show logo + title in top bar of every page."""
    logo_path = Path("assets/images/logo_cv.svg")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:14px;
                        padding:8px 0 16px 0; border-bottom:1px solid #f0f0f0;
                        margin-bottom:16px;">
                <img src="data:image/svg+xml;base64,{b64}"
                     width="48"
                     style="border-radius:50%;"/>
                <span style="font-size:22px; font-weight:900;
                             color:#DC2626; letter-spacing:-0.5px;">
                    CareerVector
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


load_theme()
selected = render_sidebar()

render_topbar()

if selected == "Home":
    render_hero()
    render_dashboard()

elif selected == "Vector Analysis":
    render_resume_analysis()

elif selected == "Career Matches":
    render_job_matches()

elif selected == "ATS Radar":
    render_ats_score()

elif selected == "Growth Path":
    render_skill_gap()

elif selected == "Vector Boost":
    render_resume_optimizer()

elif selected == "Interview Launchpad":
    render_interview_prep()