from rag_pipeline.retrieval.retriver_modules.bm25Retriever import BM25Retriever
from rag_pipeline.retrieval.retriver_modules.pathway_retriever import PathwayRetriever

class HybridRetriever:
    def __init__(self, bm25_docs: list[str], pathway_url: str):
        self.bm25 = BM25Retriever(bm25_docs)
        self.pathway = PathwayRetriever(pathway_url)

    def search(self, query: str, k: int = 20):
        bm25_hits = self.bm25.search(query, k=k)
        pathway_hits = self.pathway.search(query, k=k)

        # Normalize everything to plain text
        pathway_texts = [d.page_content for d in pathway_hits]

        # Merge & deduplicate
        merged = list(dict.fromkeys(bm25_hits + pathway_texts))
        return merged[:k]
