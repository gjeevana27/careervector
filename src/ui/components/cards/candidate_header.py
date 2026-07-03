import streamlit as st


def render_candidate(candidate):

    st.header("Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"**Name**  \n{candidate.get('name','')}")

        st.markdown(f"**Email**  \n{candidate.get('email','')}")

    with col2:

        st.markdown(f"**Phone**  \n{candidate.get('phone','')}")