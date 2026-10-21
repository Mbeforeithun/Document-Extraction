from pydantic import ValidationError
from schema import Invoice

# 1. Good data: should load fine
good = {
    "invoice_number": "INV-001",
    "invoice_date": "15-Oct-2026",
    "vendor_name": "TechNova Solutions Pvt. Ltd.",
    "customer_name": "Bright Future Technologies Pvt. Ltd.",
    "line_items": [
        {"description": "Laptop", "quantity": 2, "unit_price": 55000, "amount": 110000}
    ],
    "total_amount": 110000,
}
invoice = Invoice(**good)
print("GOOD DATA OK:", invoice.vendor_name, invoice.total_amount)
print("Missing optional field defaults to:", invoice.discount)

# 2. Bad data: total_amount is text, vendor_name is missing
bad = {**good, "total_amount": "lots of money"}
del bad["vendor_name"]

try:
    Invoice(**bad)
except ValidationError as e:
    print("\nBAD DATA REJECTED:")
    print(e)