# Purchase Order JSON Schema

This document defines the strict structure required for all purchase order (PO) extractions. Every training and evaluation example must conform exactly to this schema.

## Rules for Missing Fields
Consistency is critical for fine-tuning. If an optional field is absent in the source document, the model MUST evaluate it to `null`. It must not omit the key, nor use empty strings `""`, nor hallucinate a value.

## Required Schema Structure

```json
{
  "buyer": "string representation of the buyer/customer name",
  "supplier": "string representation of the vendor/supplier name",
  "po_number": "string representation of PO identifier",
  "date": "YYYY-MM-DD",
  "delivery_date": "YYYY-MM-DD" | null,
  "currency": "3-letter ISO code",
  "total": float,
  "items": [
    {
      "item_name": "string describing the item",
      "quantity": integer,
      "unit_price": float
    }
  ]
}
```

## Field Definitions

1. `buyer` (string): The company or individual ordering the goods or services.
2. `supplier` (string): The company or individual receiving the order and supplying the goods (vendor).
3. `po_number` (string): The unique alphanumeric identifier associated with the purchase order. Must be a string.
4. `date` (string): The date the purchase order was issued, formatted strictly as `YYYY-MM-DD`.
5. `delivery_date` (string or null): The requested or scheduled delivery date, formatted as `YYYY-MM-DD`. Set to `null` if the PO does not indicate a delivery date.
6. `currency` (string): The required currency, output as a strict 3-letter ISO 4217 string (e.g., `"USD"`, `"GBP"`).
7. `total` (float): The grand total value of the purchase order.
8. `items` (array): An array of objects representing the requested goods or services.
   - `item_name` (string): The name, product ID, or description of the requested item.
   - `quantity` (integer): The number of units ordered.
   - `unit_price` (float): The cost per requested unit.
