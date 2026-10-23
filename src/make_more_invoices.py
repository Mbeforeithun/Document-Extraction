from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def make_pdf(path, lines):
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    for line in lines:
        c.drawString(50, y, line)
        y -= 22
    c.save()
    print("Created", path)


# 005: BAD. Line item 1 should be 3 x 1,200 = 3,600, but is printed as 4,200
make_pdf("samples/invoice_005_wrong_line_item.pdf", [
    "TAX INVOICE",
    "Invoice No: BAD-2026-002",
    "Invoice Date: 21-Oct-2026",
    "Currency: INR",
    "Seller: Lakeview Furnishings Pvt. Ltd.",
    "Bill To: Harbor Offices Pvt. Ltd.",
    "",
    "1  Office Chair   Qty 3   Unit Price Rs 1,200.00   Amount Rs 4,200.00",
    "2  Desk Lamp      Qty 1   Unit Price Rs 800.00     Amount Rs 800.00",
    "",
    "Subtotal: Rs 5,000.00",
    "CGST (9%): Rs 450.00",
    "SGST (9%): Rs 450.00",
    "TOTAL AMOUNT: Rs 5,900.00",
    "AMOUNT DUE: Rs 5,900.00",
    "",
    "Synthetic invoice for testing. One line item amount is intentionally wrong.",
])

# 006: BAD. Total 12,980 minus 2,000 paid should be 10,980, but due is printed as 9,980
make_pdf("samples/invoice_006_wrong_amount_due.pdf", [
    "TAX INVOICE",
    "Invoice No: BAD-2026-003",
    "Invoice Date: 22-Oct-2026",
    "Currency: INR",
    "Seller: Orbit Networks Pvt. Ltd.",
    "Bill To: Summit Logistics Pvt. Ltd.",
    "",
    "1  Network Router  Qty 2    Unit Price Rs 3,000.00   Amount Rs 6,000.00",
    "2  Ethernet Cable  Qty 10   Unit Price Rs 500.00     Amount Rs 5,000.00",
    "",
    "Subtotal: Rs 11,000.00",
    "CGST (9%): Rs 990.00",
    "SGST (9%): Rs 990.00",
    "TOTAL AMOUNT: Rs 12,980.00",
    "Advance Paid: Rs 2,000.00",
    "AMOUNT DUE: Rs 9,980.00",
    "",
    "Synthetic invoice for testing. The amount due is intentionally wrong.",
])

# 007: GOOD. Different layout: discount + freight + IGST. The math is correct.
make_pdf("samples/invoice_007_igst_freight_good.pdf", [
    "INVOICE",
    "Invoice No: PMP-2026-310",
    "Invoice Date: 18-Oct-2026",
    "Currency: INR",
    "Seller: Delta Pumps and Valves Ltd.",
    "Bill To: Riverside Water Works",
    "",
    "1  Centrifugal Pump  Qty 2   Unit Price Rs 4,000.00   Amount Rs 8,000.00",
    "2  Gate Valve        Qty 5   Unit Price Rs 600.00     Amount Rs 3,000.00",
    "",
    "Subtotal: Rs 11,000.00",
    "Discount: -Rs 500.00",
    "Freight: Rs 400.00",
    "IGST (18%): Rs 1,962.00",
    "TOTAL AMOUNT: Rs 12,862.00",
    "AMOUNT DUE: Rs 12,862.00",
    "",
    "Synthetic invoice for testing. All figures are correct.",
])