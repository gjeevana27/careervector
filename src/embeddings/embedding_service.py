from sentence_transformers import SentenceTransformer
from src.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed(self, text: str) -> list:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list) -> list:
        return self.model.encode(texts).tolist()