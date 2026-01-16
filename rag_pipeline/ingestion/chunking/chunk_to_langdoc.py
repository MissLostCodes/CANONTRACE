from langchain_community.document_loaders import JSONLoader

def load_chunk_documents(chunk_file: str):
    loader = JSONLoader(
        file_path=chunk_file,
        jq_schema=".[]",          # iterate over chunk objects
        content_key="text",       # page_content = chunk["text"]
        metadata_func=chunk_metadata_func,
        text_content=False,
    )
    return loader.load()

def chunk_metadata_func(record: dict, metadata: dict) -> dict:
    """
    record  -> one chunk JSON object
    metadata -> auto-generated metadata (source, seq_num)
    """

    metadata.update({
        "chunk_id": record["chunk_id"],
        "parent_id": record["parent_id"],
        "novel_id": record["novel_id"],
        "chapter_index": record["chapter_index"],
        "position_in_chapter": record["position_in_chapter"],
        "characters_mentioned": record.get("characters_mentioned", []),
    })

    # flatten nested metadata
    for k, v in record.get("metadata", {}).items():
        metadata[k] = v

    return metadata

