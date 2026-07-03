import streamlit as st


def render_education(education):

    st.header("Education")

    if not education:
        st.info("No education found.")
        return

    for edu in education:

        with st.container(border=True):

            # Degree
            degree = (
                edu.get("degree")
                or edu.get("qualification")
                or edu.get("program")
                or "Degree"
            )

            st.subheader(degree)

            # Institution
            institution = (
                edu.get("institution")
                or edu.get("university")
                or edu.get("school")
                or edu.get("college")
                or ""
            )

            if institution:
                st.write(f"**{institution}**")

            # Location
            location = edu.get("location") or ""
            if location:
                st.write(f"📍 {location}")

            # GPA
            gpa = edu.get("gpa") or edu.get("cgpa") or ""
            if gpa:
                st.write(f"**GPA:** {gpa}")

            # Year / Graduation
            year = (
                edu.get("year")
                or edu.get("graduation")
                or edu.get("graduation_year")
                or edu.get("end_date")
                or ""
            )

            if year:
                st.write(f"**Graduation:** {year}")

            # Expected Graduation
            expected = (
                edu.get("expectedGraduation")
                or edu.get("expected_graduation")
                or edu.get("expected_year")
                or ""
            )

            if expected:
                st.write(f"**Expected Graduation:** {expected}")

            # Coursework
            coursework = (
                edu.get("coursework")
                or edu.get("courses")
                or edu.get("relevant_coursework")
                or []
            )

            if isinstance(coursework, str):
                coursework = [c.strip() for c in coursework.split(",")]

            if coursework:
                st.write("**Coursework:**")
                for course in coursework:
                    if course.strip():
                        st.markdown(f"- {course}")

        st.write("")