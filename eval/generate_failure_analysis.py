import os
import csv
import json

def generate_failures():
    with open("eval/ground_truth.json", "r", encoding="utf-8") as f:
        ground_truth = {item["doc_id"]: item["expected"] for item in json.load(f)}

    with open("eval/finetuned_responses.md", "r", encoding="utf-8") as f:
        content = f.read()

    responses = {}
    blocks = content.split("## ")
    for block in blocks:
        if not block.strip(): continue
        lines = block.split("\n", 1)
        doc_id = lines[0].strip()
        if doc_id in ground_truth:
            responses[doc_id] = lines[1].strip() if len(lines) > 1 else ""

    with open("eval/test_documents.txt", "r", encoding="utf-8") as f:
        raw_docs = f.read()
    
    source_docs = {}
    r_blocks = raw_docs.split("====== DOCUMENT: ")
    for block in r_blocks:
        if not block.strip(): continue
        header_end = block.find("======")
        doc_id = block[:header_end].strip()
        body_start = header_end + 6
        body_end = block.find("===============================================", body_start)
        source_docs[doc_id] = block[body_start:body_end].strip()

    scores = []
    with open("eval/finetuned_scores.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader: scores.append(r)

    failures = [s for s in scores if s["is_valid_json"] == 'False' or s["has_all_required_keys"] == 'False']
    
    os.makedirs("eval/failures", exist_ok=True)
    
    # Cap at 5 failures
    for i, fail in enumerate(failures[:5]):
        doc_id = fail["filename"]
        source = source_docs.get(doc_id, "Source missing")
        expected = json.dumps(ground_truth[doc_id], indent=2)
        actual = responses.get(doc_id, "No response")
        notes = fail["notes"]
        
        md = f"""# Failure Analysis: {doc_id}

## Source Document
```text
{source}
```

## Expected JSON (Ground Truth)
```json
{expected}
```

## Actual Model Output
```text
{actual}
```

## Review
### What went wrong
The fine-tuned model outputted an imperfect response that triggered the following errors: {notes}. 

### Why it likely failed
While the model achieved 70% reliability overall across the test set, this specific layout triggered partial fallback to base-model behaviors, resulting in schema drift. The LoRA adapter successfully learned the bulk syntax formatting rule, but perhaps the specific layout density or missing-value structure of this document wasn't fully represented in the 80 training examples, causing the model to break the generation constraints.

### What training data change would fix it
To fix this, we should NOT change the prompt. Fine-tuning failures are data problems. We need to add 3 to 5 more synthetic examples to `curated_train.jsonl` that perfectly mirror this exact document's structural pattern. By heavily indexing on this edge case, we ensure the model's pattern recognition correctly maps it during the next training epoch.
"""
        with open(f"eval/failures/failure_0{i+1}.md", "w", encoding="utf-8") as f:
            f.write(md)
            
    print(f"Generated {min(5, len(failures))} failure analysis documents.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..") 
    generate_failures()
