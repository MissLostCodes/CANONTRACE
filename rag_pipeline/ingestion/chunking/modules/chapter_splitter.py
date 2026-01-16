"""
Splits a full novel text into high-level structural sections
(CHAPTER / BOOK / PART) to create parent chunks for hierarchical
text processing pipelines.

Input:
- text (str): cleaned full novel text
- novel_id (str): stable novel identifier

Output:
- List of dicts with keys:
  { parent_id, chapter_index, chapter_title, text }

Behavior:
- Preserves chapter order and titles
- Generates deterministic parent_ids
- Falls back to a single FULL_TEXT chunk if no chapters are detected

Intended for downstream paragraph/semantic chunking and RAG systems.
"""
import re
from rag_pipeline.ingestion.utils import make_parent_id

CHAPTER_REGEX = re.compile(
    r"(?:^|\n)(CHAPTER\s+\w+|BOOK\s+\w+|PART\s+\w+)",
    re.IGNORECASE
)


def split_into_chapters(text: str, novel_id: str):
    """
    Returns list of ParentChunk-like dicts.
    """
    splits = CHAPTER_REGEX.split(text)

    chapters = []
    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        body = splits[i + 1].strip()

        chapters.append({
            "parent_id": make_parent_id(novel_id, i // 2),
            "chapter_index": i // 2,
            "chapter_title": title,
            "text": body,
        })

    # Fallback: if no chapters detected
    if not chapters:
        chapters.append({
            "parent_id": make_parent_id(novel_id, 0),
            "chapter_index": 0,
            "chapter_title": "FULL_TEXT",
            "text": text,
        })

    return chapters
