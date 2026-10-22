from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    amount: float
    decision: str


def ask_human(state: State):
    answer = interrupt(
        {"question": "The total looks wrong. Approve or reject?", "amount": state["amount"]}
    )
    return {"decision": answer}


builder = StateGraph(State)
builder.add_node("ask_human", ask_human)
builder.add_edge(START, "ask_human")
builder.add_edge("ask_human", END)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "demo-1"}}

# Run 1: starts, hits interrupt(), and pauses
first = graph.invoke({"amount": 30000.0, "decision": ""}, config)
print("PAUSED. What the human sees:", first["__interrupt__"])

# Run 2: the human answers, and the run continues from the pause
final = graph.invoke(Command(resume="approve"), config)
print("RESUMED. Decision:", final["decision"])