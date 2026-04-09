import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_evaluation():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    with open("eval/test_documents.txt", "r") as f:
        content = f.read()

    # Parse the documents from the text file layout
    docs = []
    blocks = content.split("====== DOCUMENT: ")
    for block in blocks:
        if not block.strip():
            continue
        header_end = block.find("======")
        doc_id = block[:header_end].strip()
        body_start = header_end + 6
        body_end = block.find("===============================================", body_start)
        raw_text = block[body_start:body_end].strip()
        
        if doc_id and raw_text:
            docs.append({"id": doc_id, "text": raw_text})

    print(f"Found {len(docs)} documents for evaluation.")

    instruction = "Extract all fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."

    results = []
    results.append("# Baseline Responses (Llama 3.2 3B Instruct via Groq)\n")

    for i, doc in enumerate(docs):
        print(f"Processing {i+1}/{len(docs)}: {doc['id']}")
        
        prompt = f"{instruction}\n\n{doc['text']}"
        
        try:
            # Send the exact same prompt structure to Llama 3.2 3B
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.2-3b-preview",
                temperature=0.0 # Greedy decoding for extraction tasks
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = f"ERROR: {str(e)}"
            
        results.append(f"## {doc['id']}")
        results.append("```json\n" + response + "\n```\n")
        
        # Small delay to respect free tier rate limits
        time.sleep(1)

    # Save to markdown
    with open("eval/baseline_responses.md", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print("\n✅ Successfully saved all 20 responses to eval/baseline_responses.md")

if __name__ == "__main__":
    # Ensure working directory is the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    os.chdir(project_root)
    
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: Please put your GROQ_API_KEY in a .env file first.")
        exit(1)
        
    run_evaluation()
