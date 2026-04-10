# Failure Analysis: eval_po_4

## Source Document
```text
PURCHASE REQUISITION: PO-EVAL-402
ISSUED BY: Tyrell Corp
VENDOR: SynthCorp
DATE OF ORIGIN: 2024-12-30
MUST DELIVER BY: 2025-09-04
TRADE CURRENCY: EUR
* Bulk Capacitor (Quantity: 10, Rate: 1.5)
* Bulk Sensor Array (Quantity: 37, Rate: 90.0)
* Bulk Audit Service (Quantity: 11, Rate: 204.0)
* Bulk Audit Service (Quantity: 20, Rate: 203.0)
GROSS REQUIREMENT: 9649.0
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "Tyrell Corp",
  "supplier": "SynthCorp",
  "po_number": "PO-EVAL-402",
  "date": "2024-12-30",
  "delivery_date": "2025-09-04",
  "currency": "EUR",
  "total": 9649.0,
  "items": [
    {
      "item_name": "Bulk Capacitor",
      "quantity": 10,
      "unit_price": 1.5
    },
    {
      "item_name": "Bulk Sensor Array",
      "quantity": 37,
      "unit_price": 90.0
    },
    {
      "item_name": "Bulk Audit Service",
      "quantity": 11,
      "unit_price": 204.0
    },
    {
      "item_name": "Bulk Audit Service",
      "quantity": 20,
      "unit_price": 203.0
    }
  ]
}
```

## Actual Model Output
```text
```json
{
  "vendor": "SynthCorp",
  "supplier": null,
  "po_number": "PO-EVAL-402",
  "date": "2024-12-30",
  "delivery_date": "2025-09-04",
  "currency": "EUR",
  "total": 9649.0,
  "items": [
    { "item_name": "Bulk Capacitor", "quantity": 10, "unit_price": 1.5 },
    { "item_name": "Bulk Sensor Array", "quantity": 37, "unit_price": 90.0 },
    { "item_name": "Bulk Audit Service", "quantity": 11, "unit_price": 204.0 },
    { "item_name": "Bulk Audit Service", "quantity": 20, "unit_price": 203.0 }
  ]
}
```
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: value_mismatch:supplier; missing_keys:buyer. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
