from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import read_pdf
from schema import Invoice

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
extractor = llm.with_structured_output(Invoice)

text = read_pdf.invoke({"file_path": "samples/invoice_001_standard_gst.pdf"})
invoice = extractor.invoke(
    f"Extract the invoice fields from this document:\n\n{text}"
)

print(type(invoice))
print(invoice.model_dump_json(indent=2))