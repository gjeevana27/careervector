import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Main model for heavy tasks
    MODEL_NAME = "llama-3.3-70b-versatile"

    # Lighter model for interview chat — saves tokens
    INTERVIEW_MODEL = "llama-3.1-8b-instant"

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = "jd-matcher"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    def validate(self):

        errors = []

        if not self.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is missing.")

        if not self.PINECONE_API_KEY:
            errors.append("PINECONE_API_KEY is missing.")

        if errors:
            raise ValueError("\n".join(errors))

        return True


settings = Settings()
settings.validate()