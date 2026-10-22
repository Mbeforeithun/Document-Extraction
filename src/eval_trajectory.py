import json
from langgraph.types import Command
from openevals import create_trajectory_match_evaluator
from agent import agent


def run_unattended(file_path: str):
    config = {"configurable": {"thread_id": f"eval-{file_path}"}, "recursion_limit": 25}
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
for path, expected in ground_truth.items():
    path_expected = GOOD_PATH if expected["should_pass_validation"] else BAD_PATH
    messages = run_unattended(path)
    result = evaluator(
        outputs=messages,
        reference_outputs=reference_trajectory(path_expected),
    )
    print(f"{path}: {result['key']} = {result['score']}")
    passed += bool(result["score"])

print(f"\nTrajectory match: {passed}/{len(ground_truth)}")