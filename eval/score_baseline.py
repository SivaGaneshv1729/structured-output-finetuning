import json
import csv
import re
import os

def score_baseline():
    with open("eval/ground_truth.json", "r", encoding="utf-8") as f:
        ground_truth = {item["doc_id"]: item["expected"] for item in json.load(f)}

    try:
        with open("eval/baseline_responses.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: baseline_responses.md not found.")
        return

    # Parse the markdown responses
    responses = {}
    blocks = content.split("## ")
    for block in blocks:
        if not block.strip(): continue
        lines = block.split("\n", 1)
        doc_id = lines[0].strip()
        if doc_id in ground_truth:
            raw_output = lines[1].strip() if len(lines) > 1 else ""
            responses[doc_id] = raw_output

    csv_data = []
    success_count = 0

    for doc_id, expected in ground_truth.items():
        raw_response = responses.get(doc_id, "")
        
        # Check for markdown code fences (a major parsing failure source)
        json_str = raw_response
        has_markdown = False
        if "```json" in json_str or "```" in json_str:
            has_markdown = True
            # Try to extract from within the fence
            match = re.search(r"```(?:json)?\n(.*?)\n```", json_str, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
            else:
                json_str = json_str.replace("```json", "").replace("```", "").strip()
        
        is_valid_json = False
        parsed_json = None
        try:
            parsed_json = json.loads(json_str)
            is_valid_json = True
        except Exception:
            pass
            
        has_all_required_keys = False
        key_accuracy = 0.0
        value_accuracy = 0.0
        notes = []
        
        if has_markdown: 
            notes.append("contains_markdown_fence")
            
        if not is_valid_json:
            notes.append("invalid_json_syntax")
        elif isinstance(parsed_json, dict):
            expected_keys = set(expected.keys())
            parsed_keys = set(parsed_json.keys())
            
            has_all_required_keys = expected_keys.issubset(parsed_keys)
            
            correct_keys = expected_keys.intersection(parsed_keys)
            key_accuracy = len(correct_keys) / len(expected_keys) if expected_keys else 0
            
            correct_values = 0
            for k in correct_keys:
                if parsed_json.get(k) == expected.get(k):
                    correct_values += 1
                else:
                    notes.append(f"value_mismatch:{k}")
            value_accuracy = correct_values / len(correct_keys) if correct_keys else 0
            
            if not has_all_required_keys:
                missing = expected_keys - parsed_keys
                notes.append(f"missing_keys:{','.join(missing)}")
        else:
            notes.append("parsed_json_not_an_object")
            
        if is_valid_json and has_all_required_keys:
            success_count += 1
            
        csv_data.append({
            "filename": doc_id,
            "raw_output_first_50_chars": raw_response.replace("\n", " ")[:50],
            "is_valid_json": is_valid_json,
            "has_all_required_keys": has_all_required_keys,
            "key_accuracy": round(key_accuracy, 2),
            "value_accuracy": round(value_accuracy, 2),
            "notes": "; ".join(notes) if notes else "perfect"
        })

    with open("eval/baseline_scores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)
        
    parse_success_rate = (success_count / len(ground_truth)) * 100

    summary_md = f"""# Baseline Evaluation Summary

**Baseline Parse Success Rate:** {parse_success_rate:.0f}%

Out of {len(ground_truth)} documents, the base model successfully extracted valid JSON containing all required schema keys only **{success_count}** times.

### Key Observations
* The base model frequently relies on markdown formatting (`` ```json ``), which breaks direct parsing pipelines.
* Fine-tuning with LoRA will strictly prioritize fixing this formatting instability, aiming for a consistent 95%+ parse success rate with no prose or fences.
"""

    with open("eval/summary.md", "w") as f:
        f.write(summary_md)

    print(f"Scoring complete. Parse success rate: {parse_success_rate:.1f}%")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")  # Go up to project root
    score_baseline()
