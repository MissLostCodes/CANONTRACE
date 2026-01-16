# Each chapter is a parent document with metadata: novel_id, chapter_index, chapter_title.
# Novel
#  └── Chapter (parent chunk)
#       └── Paragraph / semantic chunks (children)

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ParentChunk:
    parent_id: str
    novel_id: str
    chapter_index: int
    chapter_title: str
    text: str


@dataclass
class ChildChunk:
    chunk_id: str
    parent_id: str
    novel_id: str
    chapter_index: int
    position_in_chapter: int
    text: str
    characters_mentioned: List[str]
    metadata: Dict
