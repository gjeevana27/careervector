import streamlit as st


def render_summary(summary):

    st.header("Professional Summary")

    if not summary:
        st.info("No summary found.")
        return

    # Main summary text
    st.write(summary)

    st.divider()

    # Auto-detect keywords from the summary and highlight them
    keywords = [
        # Languages
        "Python", "SQL", "Java", "JavaScript", "C",
        # Data & ML
        "Machine Learning", "Deep Learning", "AI", "NLP",
        "Computer Vision", "Generative AI", "LLM",
        # Frameworks
        "TensorFlow", "Keras", "Scikit-learn", "PyTorch",
        "Pandas", "NumPy", "Spark", "Apache Spark",
        # Data Engineering
        "ETL", "ELT", "Airflow", "dbt", "Kafka", "Pipelines",
        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Snowflake",
        "BigQuery", "Pinecone",
        # Cloud
        "AWS", "Azure", "GCP", "Docker", "Kubernetes",
        # BI & Viz
        "Power BI", "Plotly", "Tableau", "Streamlit",
        # Roles
        "Data Science", "Data Engineer", "ML Engineer",
        "Analytics", "MLOps",
    ]

    found = [
        kw for kw in keywords
        if kw.lower() in summary.lower()
    ]

    if found:
        st.write("**Keywords:**")
        cols = st.columns(4)
        for i, kw in enumerate(found):
            cols[i % 4].info(kw)