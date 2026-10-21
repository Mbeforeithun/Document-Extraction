from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import read_pdf

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

agent = create_agent(
    llm,
    tools=[read_pdf],
    system_prompt="You are a document assistant. Use your tools to read documents.",
)

result = agent.invoke(
    {"messages": [("user", "Read samples/invoice_001_standard_gst.pdf and tell me the vendor name and the amount due.")]}
)

for msg in result["messages"]:
    msg.pretty_print()