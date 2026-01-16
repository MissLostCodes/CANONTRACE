# Normalization, boilerplate removal
import re
import ftfy

def clean_text(raw_text: str) -> str:
    """
    Normalize encoding, whitespace, and obvious boilerplate.
    """
    text = ftfy.fix_text(raw_text)

    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove common boilerplate markers (customize if needed)
    boilerplate_patterns = [
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    for pat in boilerplate_patterns:
        text = re.sub(pat, "", text, flags=re.IGNORECASE | re.DOTALL)

    return text.strip()
