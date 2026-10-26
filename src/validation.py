from schema import Invoice

TOLERANCE = 0.01  # allow tiny rounding differences


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE


def validate_invoice_data(inv: Invoice) -> list[str]:
    """Return a list of problems found. An empty list means all checks passed."""
    errors = []

    # Treat missing optional amounts as zero
    discount = inv.discount or 0.0
    freight = inv.freight or 0.0
    cgst = inv.cgst or 0.0
    sgst = inv.sgst or 0.0
    igst = inv.igst or 0.0
    paid = inv.amount_paid or 0.0

    # Check 1: each line item's qty x unit price = amount
    for i, item in enumerate(inv.line_items, start=1):
        expected = item.quantity * item.unit_price
        if not _close(expected, item.amount):
            errors.append(
                f"Line item {i} ('{item.description}'): quantity x unit_price = "
                f"{expected}, but amount is {item.amount}"
            )

    # Check 2: line items add up to the subtotal
    items_sum = sum(item.amount for item in inv.line_items)
    if inv.subtotal is not None and not _close(items_sum, inv.subtotal):
        errors.append(
            f"Line items sum to {items_sum}, but subtotal is {inv.subtotal}"
        )

    # Check 3: subtotal - discount + taxes = total
    base = inv.subtotal if inv.subtotal is not None else items_sum
    expected_total = base - discount + freight + cgst + sgst + igst
    if not _close(expected_total, inv.total_amount):
        errors.append(
            f"subtotal - discount + freight + taxes = {expected_total}, "
            f"but total_amount is {inv.total_amount}"
        )

    # Check 4: total - amount paid = amount due
    if inv.amount_due is not None:
        expected_due = inv.total_amount - paid
        if not _close(expected_due, inv.amount_due):
            errors.append(
                f"total_amount - amount_paid = {expected_due}, "
                f"but amount_due is {inv.amount_due}"
            )

    return errors