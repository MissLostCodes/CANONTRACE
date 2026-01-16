import hashlib

def _hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:8]


def make_parent_id(novel_id: str, chapter_index: int) -> str:
    return f"{novel_id}_ch_{chapter_index}"


def make_child_id(novel_id: str, chapter_index: int, pos: int) -> str:
    base = f"{novel_id}_{chapter_index}_{pos}"
    return f"chunk_{_hash(base)}"
