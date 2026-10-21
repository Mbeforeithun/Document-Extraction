from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import read_pdf
from schema import Invoice
from validation import validate_invoice_data

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
extractor = llm.with_structured_output(Invoice)

# Test 1: real extraction from invoice 2, should pass
text = read_pdf.invoke({"file_path": "samples/invoice_002_services_discount.pdf"})
invoice = extractor.invoke(f"Extract the invoice fields from this document:\n\n{text}")

print("TEST 1: real extraction")
errors = validate_invoice_data(invoice)
print("Errors:", errors if errors else "none, all checks passed")

# Test 2: corrupt the subtotal and total, should be caught
broken = invoice.model_copy(update={"subtotal": 93000.0, "total_amount": 99999.0})

print("\nTEST 2: corrupted data")
for e in validate_invoice_data(broken):
    print("-", e)