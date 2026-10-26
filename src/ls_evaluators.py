from openevals.json import create_json_match_evaluator
from openevals import create_trajectory_match_evaluator
FIELDS = ["invoice_number", "vendor_name", "total_amount", "amount_due"]

_json_match = create_json_match_evaluator(aggregator="average")


def field_accuracy(outputs: dict, reference_outputs: dict) -> dict:
    """Fractions of the four key fields the agent extracted correctly."""
    got = {f: outputs["extracted"].get(f) for f in FIELDS}
    want = {f: reference_outputs[f] for f in FIELDS}
    result = _json_match(outputs=got, reference_outputs=want)
    if isinstance(result, list):
        result = result[0]
    return {"key": "field_accuracy", "score": result["score"]}

def escalation_correct(outputs: dict, reference_outputs: dict) -> dict:
    """1 if the agent flagged exactly the invoices that should fail validation."""
    should_flag = not reference_outputs["should_pass_validation"]
    return {"key": "escalation_correct", "score": int(outputs["flagged"] == should_flag)}

_trajectory_match = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
    tool_args_match_mode="ignore",
)

GOOD_PATH = ["extract_invoice", "validate_invoice"]
BAD_PATH = ["extract_invoice", "validate_invoice", "read_pdf", "flag_for_review"]


def _as_messages(tool_names):
    """Turn a list of tool names into the message format the matcher expects."""
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


def trajectory_match(outputs: dict, reference_outputs: dict) -> dict:
    """1 if the agent called exactly the expected tools in the expected order."""
    expected = GOOD_PATH if reference_outputs["should_pass_validation"] else BAD_PATH
    result = _trajectory_match(
        outputs=_as_messages(outputs["tool_names"]),
        reference_outputs=_as_messages(expected),
    )
    if isinstance(result, list):
        result = result[0]
    return {"key": "trajectory_match", "score": result["score"]}

if __name__ == "__main__":
    # Local test with fake data: no model calls, no tokens
    reference = {
        "invoice_number": "BAD-2026-001",
        "vendor_name": "Sample Traders Pvt. Ltd.",
        "total_amount": 30000.0,
        "amount_due": 30000.0,
        "should_pass_validation": False,
    }
    all_correct = {"extracted": {
        "invoice_number": "BAD-2026-001",
        "vendor_name": "Sample Traders Pvt. Ltd.",
        "total_amount": 30000.0,
        "amount_due": 30000.0,
    }}
    one_wrong = {"extracted": {
        "invoice_number": "BAD-2026-001",
        "vendor_name": "Sample Traders Pvt. Ltd.",
        "total_amount": 25960.0,
        "amount_due": 30000.0,
    }}
    print("all correct:", field_accuracy(all_correct, reference))
    print("one wrong:  ", field_accuracy(one_wrong, reference))