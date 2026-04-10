# Prompt Engineering Iterations

To determine if advanced prompt engineering could achieve the same parse success rate as our LoRA fine-tuned model, we iterated on instructions for the base Llama 3.2 3B model.

## Version 1: Zero-Shot Strict
**Approach:** Emphasize negative constraints (telling the model what NOT to do).
```text
Extract the invoice fields.
CRITICAL INSTRUCTIONS:
- You must return ONLY a JSON object.
- NO MARKDOWN FENCES. 
- Do NOT wrap your response in ```json formatting.
- Do not explain your thought process.
- If a field is missing, strictly use the unquoted value `null`.
```

## Version 2: One-Shot Structural Template
**Approach:** Provide a hollow JSON skeleton for the model to "fill in", hoping it anchors the generation.
```text
Extract the fields from the document into this exact JSON structure. Do not output anything outside of these braces:
{
  "vendor": "",
  "invoice_number": "",
  "date": "YYYY-MM-DD",
  "due_date": null,
  "currency": "",
  "subtotal": 0.0,
  "tax": null,
  "total": 0.0,
  "line_items": [{"description": "", "quantity": 0, "unit_price": 0.0}]
}

Document: [TEXT]
```

## Version 3: Few-Shot Dynamic Examples
**Approach:** The "gold standard" of prompt engineering. We provide a fully solved example of a radically different invoice right before the target invoice, demonstrating exactly how to handle edge cases.
```text
You are a precise data extraction API.

--- Example Input ---
PROVIDER: WidgetCo | DOC: 1234 | ISSUED: 2024-01-01
CURRENCY DOMAIN: USD
1x Test Item @ 5.0/ea
BASE COST: 5.0
FINAL AMOUNT: 5.0

--- Example Output ---
{"vendor": "WidgetCo", "invoice_number": "1234", "date": "2024-01-01", "due_date": null, "currency": "USD", "subtotal": 5.0, "tax": null, "total": 5.0, "line_items": [{"description": "Test Item", "quantity": 1, "unit_price": 5.0}]}

--- Target Input ---
[TEXT]

--- Target Output ---
```
