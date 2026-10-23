from typing import Optional
from pydantic import BaseModel, Field, field_validator


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class Invoice(BaseModel):
    invoice_number: str
    invoice_date: str = Field(description="Issue date as written, e.g. 15-Oct-2026")
    due_date: Optional[str] = None
    currency: Optional[str] = None

    vendor_name: str
    vendor_gstin: Optional[str] = None
    customer_name: str

    line_items: list[LineItem]

    subtotal: Optional[float] = None
    discount: Optional[float] = Field(
        default=None, description="Discount amount as a positive number"
    )
    freight: Optional[float] = Field(
        default=None, description="Freight, shipping or handling charge as a separate summary line"
    )
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    total_amount: float
    amount_paid: Optional[float] = None
    amount_due: Optional[float] = None

    @field_validator("discount")
    @classmethod
    def discount_is_positive(cls, v):
        # models sometimes copy "-500" from the document; the rule is a positive amount
        return abs(v) if v is not None else v