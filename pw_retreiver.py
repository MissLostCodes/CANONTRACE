# from langchain_community.vectorstores import PathwayVectorClient
# client = PathwayVectorClient(url = "http://127.0.0.1:8080")
# query = "what is Marseilles ?"
# x= client.similarity_search(query , k=3)
# print(x)
#
# # y = client.similarity_search(query ,k=3 ,  metadata_filter="novel_id == `the_count_of_monte_cristo` && contains(characters_mentioned, 'Marseilles') ")
# # print(y)
#

# Load raw chunk texts for BM25
from rag_pipeline.retrieval.retriver_modules.hybrid_retrieval import HybridRetriever
from rag_pipeline.retrieval.retriver_modules.reranker import RerankedRetriever
import json

CHUNK_FILE = "chunks/novels.chunks.json"

with open(CHUNK_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)
chunk_texts = [ch["text"] for ch in chunks]

hybrid = HybridRetriever(
    bm25_docs=chunk_texts,
    pathway_url="http://127.0.0.1:8080"
)

reranked = RerankedRetriever(hybrid)

query = "what is Marseilles?"

results = reranked.search(query, k=3)

for r in results:
    print(r)
