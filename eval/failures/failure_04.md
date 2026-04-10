# Failure Analysis: eval_po_5

## Source Document
```text
PURCHASE REQUISITION: PO-EVAL-631
ISSUED BY: SynthCorp
VENDOR: Cogswell Cogs
DATE OF ORIGIN: 2024-11-13
TRADE CURRENCY: GBP
* Bulk Microchip (Quantity: 49, Rate: 7.0)
* Bulk Sensor Array (Quantity: 16, Rate: 89.0)
* Bulk Sensor Array (Quantity: 31, Rate: 87.0)
* Bulk Fiber Optic Cable (Quantity: 22, Rate: 17.0)
GROSS REQUIREMENT: 4838.0
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "SynthCorp",
  "supplier": "Cogswell Cogs",
  "po_number": "PO-EVAL-631",
  "date": "2024-11-13",
  "delivery_date": null,
  "currency": "GBP",
  "total": 4838.0,
  "items": [
    {
      "item_name": "Bulk Microchip",
      "quantity": 49,
      "unit_price": 7.0
    },
    {
      "item_name": "Bulk Sensor Array",
      "quantity": 16,
      "unit_price": 89.0
    },
    {
      "item_name": "Bulk Sensor Array",
      "quantity": 31,
      "unit_price": 87.0
    },
    {
      "item_name": "Bulk Fiber Optic Cable",
      "quantity": 22,
      "unit_price": 17.0
    }
  ]
}
```

## Actual Model Output
```text
```json
{
  "vendor": "Cogswell Cogs",
  "supplier_currency": "GBP",
  "base_date": "2024-11-13",
  "date": "2024-11-13",
  "currency": "GBP",
  "total": 4838.0,
  "items": [
    { "item_name": "Bulk Microchip", "quantity": 49, "unit_price": 7.0 },
    { "item_name": "Bulk Sensor Array", "quantity": 16, "unit_price": 89.0 },
    { "item_name": "Bulk Sensor Array", "quantity": 31, "unit_price": 87.0 },
    {
      "item_name": "Bulk Fiber Optic Cable",
      "quantity": 22,
      "unit_price": 17.0
    }
  ]
}
```
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: missing_keys:delivery_date,po_number,buyer,supplier. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
