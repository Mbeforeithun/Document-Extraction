import json
from openevals.json import create_json_match_evaluator
from tools import extract_invoice

with open("src/ground_truth.json", encoding="utf-8") as f:
    ground_truth = json.load(f)

FIELDS = ["invoice_number", "vendor_name", "total_amount", "amount_due"]

# aggregator=None gives one score per field, instead of one blended score
evaluator = create_json_match_evaluator(aggregator=None)

all_scores = []
for path, expected in ground_truth.items():
    extracted = json.loads(extract_invoice.invoke({"file_path": path}))
    outputs = {f: extracted[f] for f in FIELDS}
    reference = {f: expected[f] for f in FIELDS}

    results = evaluator(outputs=outputs, reference_outputs=reference)

    print(f"\n=== {path} ===")
    for r in results:
        print(f"  {r['key']}: {r['score']}")
        all_scores.append(r["score"])

print(f"\nField accuracy: {sum(all_scores)}/{len(all_scores)}")