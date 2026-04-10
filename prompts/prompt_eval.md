# Prompt Engineering Evaluation Results

We took the 3 worst-performing documents from the baseline evaluation (`eval_inv_1`, `eval_inv_2`, `eval_inv_3`) and ran them through the base `Llama-3.2-3B-Instruct` model using the three prompt iterations.

## Results Table

| Document | V1 (Negative Constraints) | V2 (Structural Template) | V3 (Few-Shot) | Fine-Tuned Model |
|----------|---------------------------|--------------------------|---------------|------------------|
| `eval_inv_1` | **Failed:** Included ` ```json ` fences despite explicit ALL-CAPS instructions not to. | **Failed:** Hallucinated a `due_date` because the template showed it explicitly. | **Passed:** Perfectly formatted 1-line JSON. | **Passed** |
| `eval_inv_2` | **Failed:** Added conversational text "Here is the extracted data:" before the JSON. | **Passed:** Successfully filled the template and outputted raw JSON. | **Failed:** Missed the `tax` field entirely, removing the key from the output array. | **Passed** |
| `eval_inv_3` | **Failed:** Failed to parse the array structure correctly, returning plain text lines. | **Failed:** Added trailing commas violating strict JSON. | **Failed:** Wrapped output in markdown fences again. | **Passed** |

## Conclusion
While **V3 (Few-Shot)** drastically improved the semantic accuracy of the extracted values compared to the baseline, the *formatting reliability* remained fundamentally unstable. The 3B model lacks the internal parameter capacity to consistently juggle complex negative formatting instructions ("don't use markdown") alongside complex semantic extraction tasks inside a single zero/few-shot forward pass.
