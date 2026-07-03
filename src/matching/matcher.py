import numpy as np
from pinecone import Pinecone
from src.core.config import settings
from src.embeddings.embedding_service import EmbeddingService


class JobMatcher:

    def __init__(self):
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = pc.Index(settings.PINECONE_INDEX_NAME)
        self.embedder = EmbeddingService()

    def match(
        self,
        resume_text: str,
        top_k: int = 10,
        resume: dict = None
    ) -> list:

        # Base embedding from full resume text
        resume_embedding = np.array(
            self.embedder.embed(resume_text)
        )

        # If structured resume available use weighted embedding
        if resume:
            skills = resume.get("skills", [])
            experience = resume.get("experience", [])

            skills_text = " ".join(skills) if skills else ""

            exp_text = " ".join([
                e.get("title", "") + " " +
                " ".join(e.get("achievements", []))
                for e in experience
                if isinstance(e, dict)
            ]) if experience else ""

            if skills_text and exp_text:
                skills_emb = np.array(
                    self.embedder.embed(skills_text)
                )
                exp_emb = np.array(
                    self.embedder.embed(exp_text)
                )
                resume_embedding = (
                    resume_embedding * 0.2 +
                    skills_emb * 0.4 +
                    exp_emb * 0.4
                )

            elif skills_text:
                skills_emb = np.array(
                    self.embedder.embed(skills_text)
                )
                resume_embedding = (
                    resume_embedding * 0.4 +
                    skills_emb * 0.6
                )

        results = self.index.query(
            vector=resume_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )

        matches = []
        for match in results["matches"]:
            meta = match.get("metadata", {})
            matches.append({
                "jd_id": match["id"],
                "score": round(match["score"] * 100, 1),
                "title": meta.get("title", "Unknown Role"),
                "company": meta.get("company", "Unknown Company"),
                "location": meta.get("location", ""),
                "required_skills": meta.get("required_skills", ""),
                "full_description": meta.get("full_description", ""),
                "employment_type": meta.get("employment_type", ""),
                "is_remote": meta.get("is_remote", False),
                "apply_link": meta.get("apply_link", ""),
                "posted_at": meta.get("posted_at", "")
            })

        return matches