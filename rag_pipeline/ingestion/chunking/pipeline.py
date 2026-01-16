from tqdm import tqdm
from rag_pipeline.ingestion.chunking.modules.chapter_splitter import split_into_chapters
from rag_pipeline.ingestion.chunking.modules.semantic_chunker import chunk_chapter
import json
from pathlib import Path

def load_canonical_characters(novel_dir: Path) -> dict:
    canonical_path = next(novel_dir.glob("*.canonical_characters.json"))
    with open(canonical_path, encoding="utf-8") as f:
        return json.load(f)


def chunk_novel(
    novel_path: str,
    novel_id: str,
    canonical_characters: dict
):
    print(f"Chunking novel: {novel_id}")

    with open(novel_path, encoding="utf-8") as f:
        cleaned_novel = f.read()

    chapters = split_into_chapters(cleaned_novel, novel_id)

    all_chunks = []
    for chapter in tqdm(chapters, desc=f"Chunking {novel_id}"):
        child_chunks = chunk_chapter(
            chapter,
            novel_id,
            canonical_characters
        )
        all_chunks.extend(child_chunks)

    print(f"{novel_id}: Generated {len(all_chunks)} chunks")
    return all_chunks

def chunk_all_novels(clean_data_root: str):
    clean_data_root = Path(clean_data_root)
    all_chunks = []

    for novel_dir in clean_data_root.iterdir():
        if not novel_dir.is_dir():
            continue

        novel_id = novel_dir.name

        cleaned_txt = next(novel_dir.glob("*.cleaned.txt"))
        canonical_characters = load_canonical_characters(novel_dir)

        chunks = chunk_novel(
            novel_path=str(cleaned_txt),
            novel_id=novel_id,
            canonical_characters=canonical_characters
        )

        all_chunks.extend(chunks)

    return all_chunks

