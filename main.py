from ui.app import run_app

if __name__ == "__main__":
    run_app()

#-----------------------run preprocessing pipeline -----------------------------------------
from rag_pipeline.ingestion.preprocessing.pipeline import preprocess_novel


# preprocess_novel(
#     novel_path="data/novels/In search of the castaways.txt",
#     novel_id="in_search_of_the_castaways",
#     debug=True
# )

# preprocess_novel(
#     novel_path="data/novels/The Count of Monte Cristo.txt",
#     novel_id="the_count_of_monte_cristo",
#     debug=True
# )
#-----------------------------------------------------------------------------------------------

# ----------------running chunking pipeline ---------------------------------------------------
# from rag_pipeline.ingestion.chunking.pipeline import chunk_all_novels
# all_chunks = chunk_all_novels("clean_data")
#
# import json
# from pathlib import Path
# from typing import List
#
# def save_chunks(chunks: list, output_path: Path) -> None:
#     output_path.parent.mkdir(parents=True, exist_ok=True)
#
#     serializable_chunks = [
#         chunk.__dict__ if not isinstance(chunk, dict) else chunk
#         for chunk in chunks
#     ]
#
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(serializable_chunks, f, ensure_ascii=False, indent=2)
#
#
# save_chunks(
#     all_chunks,
#     Path("chunks/novels.chunks.json")
# )

#----------------------------------------------------------------------------------------------

# ---------------pathway indexing -------------------------------------------------------------
# index_to_pathway()
#----------------------------------------------------------------------------------------------
# import json
# from pathlib import Path
#
# def json_array_to_jsonl(input_path: str, output_path: str) -> None:
#     input_path = Path(input_path)
#     output_path = Path(output_path)
#
#     with input_path.open("r", encoding="utf-8") as f:
#         data = json.load(f)   # must be a list
#
#     assert isinstance(data, list), "Input JSON must be a list of objects"
#
#     with output_path.open("w", encoding="utf-8") as f:
#         for obj in data:
#             json.dump(obj, f, ensure_ascii=False)
#             f.write("\n")
#
#     print(f"✅ Converted {len(data)} objects → {output_path}")
# json_array_to_jsonl(
#     "chunks/novels.chunks.json",
#     "chunks/novels.chunks.jsonl"
# )

