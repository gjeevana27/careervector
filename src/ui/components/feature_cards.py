import streamlit as st


def feature_card(
    title,
    description,
    button_text,
    page,
):

    with st.container(border=True):

        st.markdown(f"### {title}")

        st.write(description)

        st.write("")

        if st.button(
            button_text,
            key=f"btn_{page}",
            use_container_width=True,
        ):

            st.session_state.page = page

            st.rerun()