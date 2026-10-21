from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import read_pdf, extract_invoice, validate_invoice

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

agent = create_agent(
    llm,
    tools=[read_pdf, extract_invoice, validate_invoice],
    system_prompt=(
        "You are an invoice processing assistant. "
        "Use extract_invoice to get structured invoice data from a PDF. "
        "Always run validate_invoice on the extracted data before reporting it. "
        "Use read_pdf only when you need the raw text. "
        "In your final answer, state the vendor, the amount due, and whether validation passed."
    ),
)

result = agent.invoke(
    {"messages": [("user", "Process samples/invoice_003_multipage_equipment.pdf")]}
)

for msg in result["messages"]:
    msg.pretty_print()