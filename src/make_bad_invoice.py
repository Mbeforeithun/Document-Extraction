from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("samples/invoice_004_wrong_total.pdf", pagesize=A4)
lines = [
    "TAX INVOICE",
    "Invoice No: BAD-2026-001",
    "Invoice Date: 20-Oct-2026",
    "Currency: INR",
    "Seller: Sample Traders Pvt. Ltd.",
    "Bill To: Demo Customer Pvt. Ltd.",
    "",
    "1  Office Chair   Qty 4   Unit Price Rs 5,000.00   Amount Rs 20,000.00",
    "2  Desk Lamp      Qty 2   Unit Price Rs 1,000.00   Amount Rs 2,000.00",
    "",
    "Subtotal: Rs 22,000.00",
    "CGST (9%): Rs 1,980.00",
    "SGST (9%): Rs 1,980.00",
    "TOTAL AMOUNT: Rs 30,000.00",
    "AMOUNT DUE: Rs 30,000.00",
    "",
    "Synthetic invoice for testing. The total is intentionally wrong.",
]
y = 800
for line in lines:
    c.drawString(50, y, line)
    y -= 22
c.save()
print("Created samples/invoice_004_wrong_total.pdf")