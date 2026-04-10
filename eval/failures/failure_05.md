# Failure Analysis: eval_po_6

## Source Document
```text
PURCHASE REQUISITION: PO-EVAL-174
ISSUED BY: Sirius Cybernetics
VENDOR: Cogswell Cogs
DATE OF ORIGIN: 2024-03-06
TRADE CURRENCY: GBP
* Bulk Audit Service (Quantity: 21, Rate: 202.0)
* Bulk Audit Service (Quantity: 23, Rate: 203.0)
GROSS REQUIREMENT: 8911.0
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "Sirius Cybernetics",
  "supplier": "Cogswell Cogs",
  "po_number": "PO-EVAL-174",
  "date": "2024-03-06",
  "delivery_date": null,
  "currency": "GBP",
  "total": 8911.0,
  "items": [
    {
      "item_name": "Bulk Audit Service",
      "quantity": 21,
      "unit_price": 202.0
    },
    {
      "item_name": "Bulk Audit Service",
      "quantity": 23,
      "unit_price": 203.0
    }
  ]
}
```

## Actual Model Output
```text
```json
{
  "vendor": "Cogswell Cogs",
  "supplier": null,
  "po_number": "PO-EVAL-174",
  "date": "2024-03-06",
  "delivery_date": null,
  "currency": "GBP",
  "total": 8940.0,
  "item_list": [
    { "item_name": "Bulk Audit Service", "quantity": 21, "unit_price": 202.0 },
    { "item_name": "Bulk Audit Service", "quantity": 23, "unit_price": 203.0 }
  ],
  "tax": null,
  "subtotal": 8940.0,
  "line_items": [
    {
      "description": "Bulk Audit Service",
      "quantity": 21,
      "unit_price": 202.0,
      "total": 4242.0
    },
    {
      "description": "Bulk Audit Service",
      "quantity": 23,
      "unit_price": 203.0,
      "total": 4691.0
    }
  ]
}
```
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: value_mismatch:supplier; value_mismatch:total; missing_keys:buyer,items. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
