# Structured Output Fine-Tuning: Llama 3.2

This project fine-tunes a Llama 3.2 3B Instruct model using LoRA to reliably extract consistently keyed, machine-parseable JSON data from unstructured business documents (Invoices and Purchase Orders).

By conforming strictly to the "No Custom Python Application" rule, all execution relies entirely on UI-based fine-tuning software (LlamaFactory/Unsloth) and manual qualitative evaluation.

---

## How to Run and Reproduce This Project Manually

If you wish to independently verify the dataset, fine-tune the model yourself, and evaluate the results, follow this strict manual pipeline:

### 1. Review the Curation Rules
1. Read `schema/invoice_schema.md` and `schema/po_schema.md` to understand the strict JSON constraints and `null` handling rules.
2. The core dataset is located at `data/curated_train.jsonl`, consisting of 80 carefully constructed pairs of raw document text mapped to their mathematically perfect JSON outputs.
3. Review `data/curation_log.md` to see the qualitative selection process for maintaining layout diversity.

### 2. Run the Baseline Evaluation
1. Boot up **LlamaFactory** (or Open WebUI) in your GPU environment and load the base `Llama-3.2-3B-Instruct` model.
2. Navigate to the **Inference / Chat Tab**.
3. For an evaluation document of your choosing, paste the text alongside the structural rule: *"Extract all fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."*
4. You will observe the model frequently violating strict formatting constraints (e.g., hallucinating markdown fences).
5. Compare your manual tests against our recorded results in `eval/baseline_responses.md` and `eval/baseline_scores.csv`.

### 3. Execute LoRA Fine-Tuning
1. In LlamaFactory's **Train Tab** (or an Unsloth SFT Notebook workflow), upload `data/curated_train.jsonl` as your training dataset.
2. Configure the LoRA adapters exactly as documented in `training_config.md`:
   * **Rank ($r$):** 16
   * **Alpha ($\alpha$):** 32
   * **Target Modules:** All attention and MLP layers (`q_proj`, `v_proj`, etc.)
   * **Learning Rate:** `2e-4`
3. Hit "Train" and observe the loss curve smoothly decrease over ~10 epochs.

### 4. Post-Tuning Evaluation
1. Load your newly generated fine-tuned LoRA weights into the Inference Tab.
2. Manually query the exact same evaluation documents again.
3. You will immediately notice the complete cessation of conversational tokens and markdown fences. 
4. Calculate the new Parse Success Rate by verifying syntax validity. Compare your manual scores against our side-by-side analysis located in `eval/before_vs_after.md`.

### 5. Review Failure Analysis
Not all inferences will be perfect post-tuning. Check `eval/failures/` to review manual root-cause diagnoses on the final remaining failures, tracing them back to sparse layouts and density issues.

### 6. Prompt Engineering vs SFT Comparison
If attempting to fix baseline issues using few-shot templates instead of fine-tuning, you will find it highly token-inefficient and intrinsically brittle. See `report.md` and `prompts/prompt_iterations.md` for our manual tests and conclusions regarding the operational superiority of SFT for structured extraction.
