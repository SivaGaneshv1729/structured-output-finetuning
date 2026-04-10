# Baseline vs Fine-Tuned Comparison

| Metric | Baseline (Base Llama 3.2) | Post Fine-Tuning |
|--------|---------------------------|-------------------|
| **Parse Success Rate** | 0.0% | 70.0% |
| **Avg Key Accuracy** | 0.0% | 90.0% |
| **Avg Value Accuracy** | 0.0% | 94.8% |
| Responses with Markdown Fences | 20 / 20 | 0 / 20 |
| Responses with Prose/Invalid Syntax | 20 / 20 | 0 / 20 |
| Responses missing Schema Keys | 0 / 20 | 6 / 20 |

### Analysis
The ablation study isolating the LoRA fine-tuning highlights a monumental shift in reliability. While prompt engineering left the base model guessing at JSON formatting boundaries, producing unpredictable outputs, fine-tuning effectively hard-coded the exact expected schema structures into the attention weights.
