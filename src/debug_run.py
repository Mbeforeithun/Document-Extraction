import uuid
from langgraph.types import Command
from agent import agent

FILE = "samples/invoice_008_prompt_injection.pdf"

for attempt in range(1, 4):
    config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 25}
    result = agent.invoke({"messages": [("user", f"Process {FILE}")]}, config)
    while "__interrupt__" in result:
        result = agent.invoke(Command(resume="reject"), config)

    print(f"\n--- attempt {attempt} ---")
    for m in result["messages"]:
        for call in getattr(m, "tool_calls", None) or []:
            if call["name"] == "flag_for_review":
                print("FLAGGED, reason:", call["args"].get("reason"))
            else:
                print("called:", call["name"])
        if getattr(m, "name", None) == "validate_invoice":
            print("validate_invoice returned:", m.content)
    print("FINAL ANSWER:", result["messages"][-1].content)