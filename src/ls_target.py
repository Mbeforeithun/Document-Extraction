import json
import uuid

from langgraph.types import Command

from agent import agent


def run_agent(inputs: dict) -> dict:
    """Run the agent unattended on one invoice and return JSON-friendly results."""
    file_path = inputs["file_path"]
    config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 25}
    result = agent.invoke({"messages": [("user", f"Process {file_path}")]}, config)
    while "__interrupt__" in result:
        result = agent.invoke(Command(resume="reject"), config)

    tool_names = []
    extracted = {}
    for m in result["messages"]:
        for call in getattr(m, "tool_calls", None) or []:
            tool_names.append(call["name"])
        if getattr(m, "name", None) == "extract_invoice":
            try:
                extracted = json.loads(m.content)
            except Exception:
                pass

    return {
        "tool_names": tool_names,
        "extracted": extracted,
        "flagged": "flag_for_review" in tool_names,
        "final_answer": str(result["messages"][-1].content),
    }


if __name__ == "__main__":
    out = run_agent({"file_path": "samples/invoice_004_wrong_total.pdf"})
    print("tools:  ", out["tool_names"])
    print("flagged:", out["flagged"])
    print("total:  ", out["extracted"].get("total_amount"))
    print("answer: ", out["final_answer"][:200])