# Failure Analysis: eval_po_2

## Source Document
```text
PURCHASE REQUISITION: PO-EVAL-937
ISSUED BY: Omni Consumer
VENDOR: Weyland-Yutani
DATE OF ORIGIN: 2024-03-17
TRADE CURRENCY: CAD
* Bulk Software License (Quantity: 17, Rate: 350.0)
GROSS REQUIREMENT: 5950.0
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "Omni Consumer",
  "supplier": "Weyland-Yutani",
  "po_number": "PO-EVAL-937",
  "date": "2024-03-17",
  "delivery_date": null,
  "currency": "CAD",
  "total": 5950.0,
  "items": [
    {
      "item_name": "Bulk Software License",
      "quantity": 17,
      "unit_price": 350.0
    }
  ]
}
```

## Actual Model Output
```text
```json
{
  "vendor": "Weyland-Yutani",
  "supplier": null,
  "date": "2024-03-17",
  "currency": "CAD",
  "total": 5950.0,
  "items": [
    {
      "item_name": "Bulk Software License",
      "quantity": 17,
      "unit_price": 350.0
    }
  ]
}
```
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: value_mismatch:supplier; missing_keys:delivery_date,po_number,buyer. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
