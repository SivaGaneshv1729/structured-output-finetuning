# Baseline Evaluation Summary

**Baseline Parse Success Rate:** 0%

Out of 20 documents, the base model successfully extracted valid JSON containing all required schema keys only **0** times.

### Key Observations
* The base model frequently relies on markdown formatting (`` ```json ``), which breaks direct parsing pipelines.
* Fine-tuning with LoRA will strictly prioritize fixing this formatting instability, aiming for a consistent 95%+ parse success rate with no prose or fences.
