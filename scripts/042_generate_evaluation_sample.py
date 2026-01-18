import json
import csv
import random

# Configuration
INPUT_FILE = "optimized_records_gemini.json"
OUTPUT_FILE = "sampled_entities.csv"
TERMS_PER_RECORD = 2  # How many random terms to pick from each record's 'about' list

def generate_csv_sample():
    try:
        with open(INPUT_FILE, "r", encoding='utf-8') as f:
            records = json.load(f)
        
        csv_data = []

        for record in records:
            record_id = record.get("ID", "")
            record_name = record.get("name", "")
            record_desc = record.get("description", "")
            
            # The pool of terms to sample from
            about_list = record.get("about", [])
            
            if not about_list:
                continue

            # Identify which IDs are marked as relevant
            # We use sets of IDs for much faster lookups
            relevant_ids = {item["ID"] for item in record.get("relevant_about", [])}
            gemini_ids = {item["ID"] for item in record.get("relevant_about_gemini", [])}

            # Randomly sample terms (ensure we don't try to sample more than exist)
            sample_size = min(len(about_list), TERMS_PER_RECORD)
            sampled_terms = random.sample(about_list, sample_size)

            for term in sampled_terms:
                term_id = term.get("ID")
                
                # Check for existence in subsets
                is_relevant = "yes" if term_id in relevant_ids else "no"
                is_gemini = "yes" if term_id in gemini_ids else "no"

                csv_data.append({
                    "ID": record_id,
                    "name": record_name,
                    "description": record_desc,
                    "about_ID": term_id,
                    "about_label": term.get("label", ""),
                    "about_description": term.get("description", ""),
                    "relevant": is_relevant,
                    "relevant_gemini": is_gemini
                })

        # Write to CSV
        fieldnames = ["ID", "name", "description", "about_ID", "about_label", "about_description", "relevant", "relevant_gemini"]
        
        with open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

        print(f"Success! Processed {len(records)} records and saved sample to '{OUTPUT_FILE}'.")

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_csv_sample()