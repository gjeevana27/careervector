from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimilarityScorer:

    @staticmethod
    def score(vec1: list, vec2: list) -> float:
        a = np.array(vec1).reshape(1, -1)
        b = np.array(vec2).reshape(1, -1)
        return round(float(cosine_similarity(a, b)[0][0]) * 100, 1)