# Invoice JSON Schema

This document defines the strict structure required for all invoice extractions. Every training and evaluation example must conform exactly to this schema.

## Rules for Missing Fields
Consistency is critical for fine-tuning. If a field is present in the schema but its data is completely illegible or absent in the source document, the model MUST evaluate it to `null`. It must not omit the key, nor use empty strings `""`, nor hallucinate a value. 

## Required Schema Structure

```json
{
  "vendor": "string representation of vendor name",
  "invoice_number": "string representation of invoice identifier",
  "date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD" | null,
  "currency": "3-letter ISO code",
  "subtotal": float,
  "tax": float | null,
  "total": float,
  "line_items": [
    {
      "description": "string describing the item",
      "quantity": integer,
      "unit_price": float
    }
  ]
}
```

## Field Definitions

1. `vendor` (string): The name of the company or individual issuing the invoice.
2. `invoice_number` (string): The unique alphanumeric identifier for the invoice. Even if strictly numeric, it must be returned as a string.
3. `date` (string): The date the invoice was issued, formatted strictly as `YYYY-MM-DD`.
4. `due_date` (string or null): The deadline for payment, formatted as `YYYY-MM-DD`. Set to `null` if the source document does not mention a due date.
5. `currency` (string): The currency of the transaction, parsed into a strict 3-letter ISO 4217 string (e.g., `"USD"`, `"GBP"`, `"EUR"`, `"INR"`). If a symbol (e.g. `$`) is used, infer the ISO string.
6. `subtotal` (float): The total amount before any taxes, discounts, or additions.
7. `tax` (float or null): The total amount of tax applied. Set to `null` if missing or zero without explicitly stating so on the document.
8. `total` (float): The final payable amount on the invoice.
9. `line_items` (array): An array of objects representing items purchased. Must not be empty. If individual items cannot be parsed, extract the highest level summary available.
   - `description` (string): Name or details of the purchased good/service.
   - `quantity` (integer): The number of units purchased. Default to `1` if implied but not stated.
   - `unit_price` (float): The cost per single unit.
