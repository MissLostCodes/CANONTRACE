from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

from rag_pipeline.ingestion.chunking.schemas.schemas import ChildChunk
from rag_pipeline.ingestion.utils import make_child_id
from rag_pipeline.ingestion.chunking.modules.character_extractor import extract_characters


def chunk_chapter(
    chapter: dict,
    novel_id: str,
    canonical_characters: dict,
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        separators=["\n\n", ".", "?", "!"]
    )

    raw_chunks = splitter.split_text(chapter["text"])
    child_chunks = []

    for idx, chunk_text in enumerate(raw_chunks):
        chars = extract_characters(chunk_text, canonical_characters)

        child_chunks.append(
            ChildChunk(
                chunk_id=make_child_id(
                    novel_id,
                    chapter["chapter_index"],
                    idx
                ),
                parent_id=chapter["parent_id"],
                novel_id=novel_id,
                chapter_index=chapter["chapter_index"],
                position_in_chapter=idx,
                text=chunk_text,
                characters_mentioned=chars,
                metadata={
                    "chapter_title": chapter["chapter_title"],
                    "splitter": "recursive_v1"
                }
            )
        )

    return child_chunks
