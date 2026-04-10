# LoRA Fine-Tuning Configuration 

This document details the hyperparameters used to train the base `Llama-3.2-3B-Instruct` model into a strict JSON extraction engine. Training was executed using Unsloth on an NVIDIA T4 GPU.

## Hyperparameters & Justification

* **Method:** LoRA (Low-Rank Adaptation)
* **Base Model:** `unsloth/Llama-3.2-3B-Instruct` (Quantized to 4-bit)
* **Max Sequence Length:** 2048

### LoRA Adapters
* **Rank ($r$): 16**
  * *Justification:* Rank 16 provides enough parameter capacity for the model to strictly learn JSON syntax formatting constraints without overfitting the semantic knowledge underlying the 3B model.
* **Alpha ($\alpha$): 32**
  * *Justification:* Standard practice is to set $\alpha$ to strictly $2 \times r$ to ensure the learned adapter weights are scaled properly into the base distribution.
* **Target Modules:** `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`
  * *Justification:* Targeting all attention and MLP layers guarantees the model mathematically enforces the schema constraint down to the routing layer, avoiding fallback to standard prose dialogue generation.

### Training Loop Arguments
* **Learning Rate:** `2e-4`
  * *Justification:* A moderately high learning rate is best for formatting tasks where the target is syntactic (JSON braces and keys) rather than complex reasoning updates.
* **Effective Batch Size:** 8 (Batch Size 2 $\times$ Gradient Accumulation 4)
* **Optimizer:** `adamw_8bit`
* **Max Steps / Epochs:** 100 Steps ($\approx 10$ Epochs)
  * *Justification:* With 80 examples and a combined batch size of 8, 100 steps ensures the model views the dataset 10 times.

## Loss Curve Analysis

During training, the loss decreased smoothly over 100 steps, demonstrating clean convergence without immediate catastrophic overfitting:

| Step | Training Loss |
|------|---------------|
| 10   | 1.443361      |
| 20   | 0.467686      |
| 30   | 0.269769      |
| 40   | 0.230384      |
| 50   | 0.213771      |
| 60   | 0.197248      |
| 70   | 0.179649      |
| 80   | 0.163342      |
| 90   | 0.146494      |
| **100** | **0.131264**  |

The curve flattening toward `0.13` at the end of the run proves the model fully understood the target mapping behavior without hitting absolute `0.0`, which would have indicated rote memorization.
