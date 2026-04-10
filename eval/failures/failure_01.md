# Failure Analysis: eval_po_1

## Source Document
```text
PURCHASE REQUISITION: PO-EVAL-172
ISSUED BY: Buy n Large
VENDOR: Weyland-Yutani
DATE OF ORIGIN: 2024-12-23
TRADE CURRENCY: CAD
* Bulk Audit Service (Quantity: 45, Rate: 202.0)
* Bulk Microchip (Quantity: 23, Rate: 10.0)
* Bulk Microchip (Quantity: 13, Rate: 7.0)
* Bulk Fiber Optic Cable (Quantity: 18, Rate: 15.0)
GROSS REQUIREMENT: 9681.0
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "Buy n Large",
  "supplier": "Weyland-Yutani",
  "po_number": "PO-EVAL-172",
  "date": "2024-12-23",
  "delivery_date": null,
  "currency": "CAD",
  "total": 9681.0,
  "items": [
    {
      "item_name": "Bulk Audit Service",
      "quantity": 45,
      "unit_price": 202.0
    },
    {
      "item_name": "Bulk Microchip",
      "quantity": 23,
      "unit_price": 10.0
    },
    {
      "item_name": "Bulk Microchip",
      "quantity": 13,
      "unit_price": 7.0
    },
    {
      "item_name": "Bulk Fiber Optic Cable",
      "quantity": 18,
      "unit_price": 15.0
    }
  ]
}
```

## Actual Model Output
```text
```json
{
  "vendor": "Weyland-Yutani",
  "supplier_currency": "CAD",
  "delivery_date": "2024-12-23",
  "currency": "CAD",
  "base_date": "2024-12-23",
  "delivery_location": "Buy n Large",
  "po_number": "PO-EVAL-172",
  "total_value": 9681.0,
  "items": [
    { "item_name": "Bulk Audit Service", "quantity": 45, "unit_price": 202.0 },
    { "item_name": "Bulk Microchip", "quantity": 23, "unit_price": 10.0 },
    { "item_name": "Bulk Microchip", "quantity": 13, "unit_price": 7.0 },
    {
      "item_name": "Bulk Fiber Optic Cable",
      "quantity": 18,
      "unit_price": 15.0
    }
  ]
}
```
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: value_mismatch:delivery_date; missing_keys:total,buyer,supplier,date. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
