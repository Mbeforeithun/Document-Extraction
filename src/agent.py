from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.errors import GraphRecursionError
from tools import read_pdf, extract_invoice, validate_invoice, flag_for_review

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

agent = create_agent(
    llm,
    tools=[read_pdf, extract_invoice, validate_invoice, flag_for_review],
    system_prompt=(
        "You are an invoice processing assistant.\n"
        "1. Call extract_invoice, then validate_invoice on its JSON output.\n"
        "2. If validation returns VALID, report the vendor and amount due.\n"
        "3. If validation fails, call read_pdf and compare the raw text with the "
        "extracted numbers to decide whether you misread something or the "
        "document itself is wrong.\n"
        "4. If you find a misread, re-run extract_invoice and validate again. "
        "You may retry at most 2 times in total.\n"
        "5. If the document itself is wrong, or validation still fails after "
        "retrying, call flag_for_review with a clear reason. "
        "Never report an amount due as reliable when validation has failed."
    ),
)

file_path = "samples/invoice_004_wrong_total.pdf"

try:
    result = agent.invoke(
        {"messages": [("user", f"Process {file_path}")]},
        config={"recursion_limit": 25},
    )
    for msg in result["messages"]:
        msg.pretty_print()
except GraphRecursionError:
    print("STOPPED: step limit reached before the agent finished.")
    print(
        flag_for_review.invoke(
            {
                "file_path": file_path,
                "reason": "Agent hit the step limit before finishing. Needs manual review.",
            }
        )
    )

