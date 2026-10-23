import json
from tools import extract_invoice

FILE = "samples/invoice_008_prompt_injection.pdf"

for attempt in range(1, 6):
    data = json.loads(extract_invoice.invoke({"file_path": FILE}))
    print(f"attempt {attempt}: total_amount={data['total_amount']}, amount_due={data['amount_due']}")