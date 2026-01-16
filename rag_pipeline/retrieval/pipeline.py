# Hybrid Retrieval + Rerank + Yes/No QA over novels
# --------------------------------------------------
#metadat filtering to be applied in future
import os
import json
from typing import List, Dict, Any

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PathwayVectorClient

from langchain.retrievers import BM25Retriever
from langchain.schema import Document
from langchain.llms import ChatOpenAI

from sentence_transformers import CrossEncoder

# # take into account only sources modified later than unix timestamp
# docs = client.similarity_search(query, metadata_filter="modified_at >= `1702672093`")
#
# # take into account only sources modified later than unix timestamp
# docs = client.similarity_search(query, metadata_filter="owner == `james`")
#
# # take into account only sources with path containing 'repo_readme'
# docs = client.similarity_search(query, metadata_filter="contains(path, 'repo_readme')")
#
# # and of two conditions
# docs = client.similarity_search(
#     query, metadata_filter="owner == `james` && modified_at >= `1702672093`"
# )
#
# # or of two conditions
# docs = client.similarity_search(
#     query, metadata_filter="owner == `james` || modified_at >= `1702672093`"
# )
# ---------------- CONFIG ----------------

PATHWAY_HOST = "http://localhost"
PATHWAY_PORT = 8080

EMBEDDING_MODEL = "intfloat/e5-large-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K_VECTOR = 30
TOP_K_BM25 = 20
TOP_K_RERANK = 8

# ----------------------------------------


class HybridNovelRetriever:
    def __init__(self, chunks_json_path: str):
        # ---- Vector store client ----
        self.vectorstore = PathwayVectorClient(
            host=PATHWAY_HOST,
            port=PATHWAY_PORT,
            embedding=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL),
        )

        # ---- Load chunks for BM25 ----
        with open(chunks_json_path, encoding="utf-8") as f:
            raw_chunks = json.load(f)

        self.documents = [
            Document(
                page_content=ch["text"],
                metadata=ch,
            )
            for ch in raw_chunks
        ]

        self.bm25 = BM25Retriever.from_documents(self.documents)
        self.bm25.k = TOP_K_BM25

        # ---- Reranker ----
        self.reranker = CrossEncoder(RERANK_MODEL)

    # --------------------------------------------------

    def retrieve(
        self,
        question: str,
        novel_id: str,
        character_id: str,
    ) -> List[Document]:

        # -------- Vector search (Pathway) --------
        vector_docs = self.vectorstore.similarity_search(
            query=question,
            k=TOP_K_VECTOR,
            filter={
                "novel_id": novel_id,
                "characters_mentioned": character_id,
            },
        )

        # -------- Lexical BM25 search --------
        bm25_docs = self.bm25.get_relevant_documents(
            f"{character_id} {question}"
        )

        # -------- Hybrid merge --------
        doc_map = {}

        for d in vector_docs + bm25_docs:
            key = (d.page_content[:100], d.metadata.get("chunk_id"))
            doc_map[key] = d

        merged_docs = list(doc_map.values())

        # -------- Reranking --------
        pairs = [(question, d.page_content) for d in merged_docs]
        scores = self.reranker.predict(pairs)

        reranked = sorted(
            zip(merged_docs, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [doc for doc, _ in reranked[:TOP_K_RERANK]]


# --------------------------------------------------


class YesNoQAModel:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
        )

    def answer(
        self,
        question: str,
        character: str,
        novel_id: str,
        context_docs: List[Document],
    ) -> Dict[str, Any]:

        context = "\n\n".join(
            f"[Chapter {d.metadata.get('chapter_index')}] {d.page_content}"
            for d in context_docs
        )

        prompt = f"""
You are a literary QA assistant.

Answer ONLY from the context.
If the answer cannot be determined, respond "unknown".

Return STRICT JSON with keys:
answer: "yes" | "no" | "unknown"
confidence: float (0 to 1)
evidence: short quoted span
reason: one sentence explanation

Character: {character}
Novel: {novel_id}

Question:
{question}

Context:
{context}
"""

        response = self.llm.invoke(prompt)
        return json.loads(response)


# --------------------------------------------------


class NovelQAPipeline:
    def __init__(self, chunks_path: str):
        self.retriever = HybridNovelRetriever(chunks_path)
        self.qa_model = YesNoQAModel()

    def run(
        self,
        novel_id: str,
        character_id: str,
        question: str,
    ) -> Dict[str, Any]:

        docs = self.retriever.retrieve(
            question=question,
            novel_id=novel_id,
            character_id=character_id,
        )

        answer = self.qa_model.answer(
            question=question,
            character=character_id,
            novel_id=novel_id,
            context_docs=docs,
        )

        return {
            "novel_id": novel_id,
            "character": character_id,
            "question": question,
            **answer,
            "retrieved_chunks": [
                {
                    "chunk_id": d.metadata.get("chunk_id"),
                    "chapter_index": d.metadata.get("chapter_index"),
                }
                for d in docs
            ],
        }
