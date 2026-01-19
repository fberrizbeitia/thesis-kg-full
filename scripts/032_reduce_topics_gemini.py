import json
import time
import os
from google import genai
from google.genai import types

# 1. Initialize the Client
# Security Note: It is best practice to use os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key="GEMINI_API_KEY")


# Filename for results
output_file = "optimized_records_gemini.json"

# --- LOAD DATA ---

try:
    with open("optimized_records.json", "r", encoding='utf-8') as f:
        linked_records = json.load(f)
except FileNotFoundError:
    print("Error: optimized_records.json not found.")
    linked_records = []

# --- LOAD EXISTING PROGRESS (to resume if interrupted) ---
if os.path.exists(output_file):
    with open(output_file, "r", encoding='utf-8') as f:
        try:
            optimized_records = json.load(f)
            processed_ids = {r.get("ID") for r in optimized_records}
            print(f"Resuming: {len(processed_ids)} records already processed.")
        except json.JSONDecodeError:
            optimized_records = []
            processed_ids = set()
else:
    optimized_records = []
    processed_ids = set()

# System Instruction
sys_instruct = (
    "You are a strict relevance evaluator. For each 'entity description' provided, "
    "determine if it is directly relevant to the 'abstract'. Respond ONLY with "
    "a JSON object in this format: {'relevant': 'yes'} or {'relevant': 'no'}."
)

# --- MAIN LOOP ---
for record in linked_records:
    record_id = record.get("ID")
    
    # Skip if already processed in a previous run OR if not in sample
    if record_id in processed_ids:
        continue
        

    abstract = record.get("description", "")
    if not abstract:
        continue 
    
    entities = record.get("about", [])
    relevant_entities = []
    
    print(f"\nProcessing: {record.get('name', 'Unknown Title')} (ID: {record_id})")  
    
    for entity in entities:
        entity_json = json.dumps(entity)
        prompt_text = f"entity description: {entity_json}\n\nabstract: {abstract}"

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct,
                    response_mime_type="application/json"
                ),
                contents=prompt_text
            )

            raw_text = response.text
            try:
                response_data = json.loads(raw_text)
                if response_data.get('relevant') == 'yes':
                    relevant_entities.append(entity)
                print(f"  - Entity Result: {response_data.get('relevant')}")
            except json.JSONDecodeError:
                print("  ! Error decoding JSON. Skipping entity.")

            time.sleep(2) # Rate limit protection

        except Exception as e:
            print(f"  ! API Error: {e}")
            if "429" in str(e):
                print("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
            continue

    # Update record and internal list
    record["relevant_about_gemini"] = relevant_entities
    optimized_records.append(record)
    processed_ids.add(record_id)

    # --- INCREMENTAL SAVE ---
    # We overwrite the file with the updated list after every record
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(optimized_records, f, indent=4, ensure_ascii=False)
    
    print(f"Saved progress to {output_file}")

print("\n--- Processing Complete ---")