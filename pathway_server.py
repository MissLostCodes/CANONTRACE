#
# import os
# import json
# import pathway as pw
# from dotenv import load_dotenv
# from pathway.xpacks.llm.vector_store import VectorStoreServer
# from pathway.xpacks.llm import embedders
#
#
# load_dotenv()
#
# CHUNK_FILE = "chunks/novels.chunks.json"
# print(f"[+] Reading {CHUNK_FILE} …")
# with open(CHUNK_FILE, encoding="utf-8") as f:
#     chunks = json.load(f)
# print(f"[+] Loaded {len(chunks)} chunks")
#
#
# class ChunkSchema(pw.Schema):
#     data: str
#     _metadata: pw.Json
#
#
# rows = [
#     (ch["text"], pw.Json({**ch, "text": ch["text"]}))
#     for ch in chunks
# ]
# print("--------------rows -------------")
# print(rows[0])
# print("--------------------------------")
# print(rows[100])
# print("--------------rows end---------------")
#
# docs = pw.debug.table_from_rows(schema=ChunkSchema, rows=rows)
# print("[+] Pathway table created")
#
# print("--------------docs--------------")
# print(docs.schema)
# print("--------------docs end---------------")
#
# embedder = embedders.SentenceTransformerEmbedder(model="sentence-transformers/all-MiniLM-L6-v2" , device="cuda" )
# print(embedder)
#
# PORT = int(os.getenv("PORT", 8080))
# server = VectorStoreServer(
#     docs,
#     embedder=embedder,
#     parser=None,
#     splitter=None,
# )
# print(server)
# print(f"[+] Starting server on 0.0.0.0:{PORT}")
# server.run_server(host="0.u0.0.0", port=PORT, threaded=False)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# import os
# import json
# import pathway as pw
# from dotenv import load_dotenv
# from pathway.xpacks.llm.vector_store import VectorStoreServer
# from pathway.xpacks.llm import embedders
#
# # -------------------------------------------------
# # Environment
# # -------------------------------------------------
# load_dotenv()
# PORT = int(os.getenv("PORT", 8080))
#
# CHUNK_FILE = "chunks/novels.chunks.json"
#
#
# # -------------------------------------------------
# # Load child chunks
# # -------------------------------------------------
# print(f"[+] Loading chunks from {CHUNK_FILE}")
#
# with open(CHUNK_FILE, encoding="utf-8") as f:
#     child_chunks = json.load(f)
#
# print(f"[+] Loaded {len(child_chunks)} child chunks")
#
#
# # -------------------------------------------------
# # Pathway Schema (FILTERABLE + PRESERVED)
# # -------------------------------------------------
# class ChunkSchema(pw.Schema):
#     # embedding input
#     data: str
#
#     # identity
#     chunk_id: str
#     parent_id: str
#
#     # parent metadata (denormalized)
#     novel_id: str
#     chapter_index: int
#     chapter_title: str
#
#     # child metadata
#     position_in_chapter: int
#     characters_mentioned: list[str]
#
#     # provenance
#     splitter: str
#
#
# # -------------------------------------------------
# # Build rows (THIS IS THE KEY PART)
# # -------------------------------------------------
# rows = []
#
# for ch in child_chunks:
#     rows.append(
#         (
#             ch["text"],                     # data → embedding
#
#             ch["chunk_id"],
#             ch["parent_id"],
#
#             ch["novel_id"],
#             ch["chapter_index"],
#             ch["metadata"]["chapter_title"],
#
#             ch["position_in_chapter"],
#             ch.get("characters_mentioned", []),
#
#             ch["metadata"].get("splitter", "unknown"),
#         )
#     )
#
# print("-------------- SAMPLE ROW --------------")
# print(rows[0])
# print("----------------------------------------")
#
#
# # -------------------------------------------------
# # Create Pathway table
# # -------------------------------------------------
# docs = pw.debug.table_from_rows(
#     schema=ChunkSchema,
#     rows=rows,
# )
#
# print("[+] Pathway table created")
# print("-------------- SCHEMA --------------")
# print(docs.schema)
# print("------------------------------------")
#
#
# # -------------------------------------------------
# # Embedder
# # -------------------------------------------------
# embedder = embedders.SentenceTransformerEmbedder(
#     model="sentence-transformers/all-MiniLM-L6-v2",
#     device="cuda",   # change to "cpu" if needed
# )
#
# print("[+] Embedder initialized")
#
#
# # -------------------------------------------------
# # Vector Store Server
# # -------------------------------------------------
# server = VectorStoreServer(
#     docs,
#     embedder=embedder,
#     parser=None,
#     splitter=None,
# )
#
# print(f"[+] Starting VectorStoreServer on 0.0.0.0:{PORT}")
#
# server.run_server(
#     host="0.0.0.0",
#     port=PORT,
#     threaded=False,
# )


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
import os
import json
import pathway as pw
from dotenv import load_dotenv
from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm import embedders

load_dotenv()
PORT = int(os.getenv("PORT", 8080))

CHUNK_FILE = "chunks/novels.chunks.json"

print(f"[+] Loading chunks from {CHUNK_FILE}")
with open(CHUNK_FILE, encoding="utf-8") as f:
    chunks = json.load(f)

print(f"[+] Loaded {len(chunks)} child chunks")


# -------------------------------------------------
# Pathway Schema (FLATTENED + _metadata SHIM)
# -------------------------------------------------
class ChunkSchema(pw.Schema):
    # embedding input (MUST BE BYTES)
    data: bytes

    # identity
    chunk_id: str
    parent_id: str

    # parent metadata
    novel_id: str
    chapter_index: int
    chapter_title: str

    # child metadata
    position_in_chapter: int
    characters_mentioned: list[str]

    # provenance
    splitter: str

    # Pathway compatibility (do NOT rely on this)
    _metadata: pw.Json


# -------------------------------------------------
# Build rows
# -------------------------------------------------
rows = []

for ch in chunks:
    rows.append(
        (
            ch["text"].encode("utf-8"),  # ✅ FIX 1

            ch["chunk_id"],
            ch["parent_id"],

            ch["novel_id"],
            ch["chapter_index"],
            ch["metadata"]["chapter_title"],

            ch["position_in_chapter"],
            ch.get("characters_mentioned", []),

            ch["metadata"].get("splitter", "unknown"),

            # metadata shim
            pw.Json({
                "novel_id": ch["novel_id"],
                "chapter_index": ch["chapter_index"],
                "chapter_title": ch["metadata"]["chapter_title"],
                "parent_id": ch["parent_id"],
                "position_in_chapter": ch["position_in_chapter"],
                "characters_mentioned": ch.get("characters_mentioned", []),
            }),
        )
    )

print("-------------- SAMPLE ROW --------------")
print(rows[0])
print("----------------------------------------")


# -------------------------------------------------
# Create table
# -------------------------------------------------
docs = pw.debug.table_from_rows(
    schema=ChunkSchema,
    rows=rows,
)

print("[+] Pathway table created")
print(docs.schema)


# -------------------------------------------------
# Embedder
# -------------------------------------------------
embedder = embedders.SentenceTransformerEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2",
    device="cuda",
)

print("[+] Embedder initialized")


# -------------------------------------------------
# Vector Store Server
# -------------------------------------------------
server = VectorStoreServer(
    docs,
    embedder=embedder,
    parser=None,
    splitter=None,
)

print(f"[+] Starting VectorStoreServer on 0.0.0.0:{PORT}")

server.run_server(
    host="0.0.0.0",
    port=PORT,
    threaded=False,
)
