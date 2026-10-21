from pypdf import PdfReader
from langchain_core.tools import tool

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from schema import Invoice
import json
from validation import validate_invoice_data

load_dotenv()


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


_extractor = ChatGroq(
    model="openai/gpt-oss-120b", temperature=0
).with_structured_output(Invoice)


@tool
def extract_invoice(file_path: str) -> str:
    """Extract structured invoice fields (vendor, customer, line items,
    taxes, totals) from a text-based PDF invoice and return them as JSON.
    Use this when you need the invoice data in structured form."""
    text = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in text.pages)
    if not text.strip():
        return "WARNING: No text found. This PDF may be scanned."
    invoice = _extractor.invoke(
        f"Extract the invoice fields from this document:\n\n{text}"
    )
    return invoice.model_dump_json(indent=2)

@tool
def validate_invoice(invoice_json: str) -> str:
    """Check extracted invoice data for math errors. Pass the JSON string
    returned by extract_invoice. Returns 'VALID' if all checks pass, or a
    list of specific problems found (for example, line items that do not
    add up to the subtotal)."""
    try:
        invoice = Invoice(**json.loads(invoice_json))
    except Exception as e:
        return f"INVALID STRUCTURE: {e}"
    errors = validate_invoice_data(invoice)
    if not errors:
        return "VALID"
    return "VALIDATION ERRORS:\n" + "\n".join(f"- {e}" for e in errors)