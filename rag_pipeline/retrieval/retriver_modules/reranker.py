from sentence_transformers import CrossEncoder
from rag_pipeline.retrieval.retriver_modules.hybrid_retrieval import HybridRetriever

class RerankedRetriever:
    def __init__(self, hybrid: HybridRetriever):
        self.hybrid = hybrid
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L12-v2")

    def search(self, query: str, k: int = 5):
        candidates = self.hybrid.search(query, k=20)
        pairs = [(query, doc) for doc in candidates]
        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc for doc, _ in ranked[:k]]
