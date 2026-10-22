import json
import uuid
from langgraph.types import Command
from openevals import create_trajectory_match_evaluator
from agent import agent


def run_unattended(file_path: str):
    # fresh thread_id per run, so runs never share saved state
    config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 25}
    result = agent.invoke({"messages": [("user", f"Process {file_path}")]}, config)
    while "__interrupt__" in result:
        result = agent.invoke(Command(resume="reject"), config)
    return result["messages"]


def reference_trajectory(tool_names):
    """Build the expected message history from a list of tool names."""
    messages = [{"role": "user", "content": "Process the invoice"}]
    for name in tool_names:
        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [{"function": {"name": name, "arguments": "{}"}}],
        })
        messages.append({"role": "tool", "content": "result"})
    messages.append({"role": "assistant", "content": "done"})
    return messages


GOOD_PATH = ["extract_invoice", "validate_invoice"]
BAD_PATH = ["extract_invoice", "validate_invoice", "read_pdf", "flag_for_review"]

evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
    tool_args_match_mode="ignore",
)

with open("src/ground_truth.json", encoding="utf-8") as f:
    ground_truth = json.load(f)

passed = 0
tp = fp = fn = tn = 0  # escalation counts

for path, expected in ground_truth.items():
    needs_review = not expected["should_pass_validation"]
    path_expected = BAD_PATH if needs_review else GOOD_PATH
    messages = run_unattended(path)

    result = evaluator(
        outputs=messages,
        reference_outputs=reference_trajectory(path_expected),
    )
    print(f"{path}: {result['key']} = {result['score']}")
    passed += bool(result["score"])

    flagged = any(
        call["name"] == "flag_for_review"
        for m in messages
        for call in (getattr(m, "tool_calls", None) or [])
    )
    tp += flagged and needs_review
    fp += flagged and not needs_review
    fn += (not flagged) and needs_review
    tn += (not flagged) and not needs_review

print(f"\nTrajectory match: {passed}/{len(ground_truth)}")
print(f"Escalation  TP={tp} FP={fp} FN={fn} TN={tn}")
print(f"Escalation recall:    {tp / (tp + fn) if (tp + fn) else 'n/a'}")
print(f"Escalation precision: {tp / (tp + fp) if (tp + fp) else 'n/a'}")