import re
from typing import List

def chunk_text(text: List[str], chunk_size: int = 500) -> List[str]:
    """
    Splits a list of text strings into smaller chunks.
    """
    if not isinstance(text, list) or not all(isinstance(page, str) for page in text):
        raise ValueError("Input text must be a list of strings")

    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer")

    chunks = []
    for page_text in text:
        try:
            # Split the text into sentences
            sentences = re.split(r"(?<=[.!?])\s+", page_text.strip())
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= chunk_size:
                    current_chunk += (" " if current_chunk else "") + sentence
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence

            if current_chunk:
                chunks.append(current_chunk)

        except Exception as e:
            raise Exception(f"Error processing text: {e}")

    return chunks
