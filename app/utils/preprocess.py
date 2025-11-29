import re

def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Lowercase
    - Remove extra whitespace
    - Remove special characters (optional, keeping it simple for now)
    """
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
