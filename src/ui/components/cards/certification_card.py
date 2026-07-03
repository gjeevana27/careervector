import streamlit as st


def render_certifications(certifications):

    st.header("Certifications")

    if not certifications:
        st.info("No certifications found.")
        return

    for cert in certifications:

        with st.container(border=True):

            # Name — matches prompt key exactly
            name = (
                cert.get("name")
                or cert.get("certification_name")
                or cert.get("title")
                or "Untitled Certification"
            )

            st.subheader(name)

            # Issuer
            issuer = (
                cert.get("issuer")
                or cert.get("organization")
                or cert.get("provider")
                or ""
            )

            if issuer:
                st.write(f"**Issuer:** {issuer}")

            # Year
            year = (
                cert.get("year")
                or cert.get("date")
                or cert.get("issued")
                or ""
            )

            if year:
                st.write(f"**Year:** {year}")

        st.write("")