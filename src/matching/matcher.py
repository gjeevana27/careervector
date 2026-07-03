import numpy as np
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from src.core.config import settings
from src.embeddings.embedding_service import EmbeddingService
import time


class JobMatcher:

    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        self.embedder = EmbeddingService()
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def ingest_jobs(self, jobs: list):
        """
        Embed and upsert new jobs to Pinecone.
        Clears existing vectors first so results are always fresh.
        """
        if not jobs:
            return

        # Clear existing vectors
        try:
            self.index.delete(delete_all=True)
            time.sleep(2)
        except Exception:
            pass

        # Embed and upsert in batches
        batch_size = 50
        for i in range(0, len(jobs), batch_size):
            batch = jobs[i:i+batch_size]

            texts = [
                (j.get("title", "") + ". " +
                 j.get("full_description", ""))
                for j in batch
            ]

            embeddings = self.model.encode(
                texts,
                show_progress_bar=False
            ).tolist()

            vectors = []
            for k, job in enumerate(batch):
                if not job.get("id"):
                    continue
                vectors.append({
                    "id": str(job["id"]),
                    "values": embeddings[k],
                    "metadata": {
                        "title": str(job.get("title", "")),
                        "company": str(job.get("company", "")),
                        "location": str(job.get("location", "") or ""),
                        "required_skills": str(
                            job.get("required_skills", "") or ""
                        )[:500],
                        "full_description": str(
                            job.get("full_description", "") or ""
                        )[:1000],
                        "employment_type": str(
                            job.get("employment_type", "") or ""
                        ),
                        "is_remote": bool(
                            job.get("is_remote", False)
                        ),
                        "apply_link": str(
                            job.get("apply_link", "") or ""
                        ),
                        "posted_at": str(
                            job.get("posted_at", "") or ""
                        )
                    }
                })

            if vectors:
                self.index.upsert(vectors=vectors)

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

        # Weighted embedding using skills + experience
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