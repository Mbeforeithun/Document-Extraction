from pypdf import PdfReader
from langchain_core.tools import tool


@tool
def read_pdf(file_path: str) -> str:
    """Read a text-based PDF file and return all its text.
    Use this first when you need the contents of a document.
    Returns a warning if the PDF has no extractable text."""
    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        return "WARNING: No text found. This PDF may be scanned."
    return text