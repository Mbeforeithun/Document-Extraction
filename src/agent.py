from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import read_pdf, extract_invoice

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

agent = create_agent(
    llm,
    tools=[read_pdf, extract_invoice],
    system_prompt=(
        "You are an invoice processing assistant. "
        "Use extract_invoice to get structured invoice data from a PDF. "
        "Use read_pdf only when you need the raw text."
    ),
)

result = agent.invoke(
    {"messages": [("user", "Extract the data from samples/invoice_002_services_discount.pdf and give me the vendor, the discount, and the amount due.")]}
)

for msg in result["messages"]:
    msg.pretty_print()