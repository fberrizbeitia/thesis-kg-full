#open optimized_records.json and compare the entities in the "relevant_about" field with the entities in the "about" field of the original records. Count how many entities are in the "relevant_about" field and how many are in the "about" field. Print the results.
import json

# Load the optimized records
with open("optimized_records.json", "r", encoding='utf-8') as f:
    optimized_records = json.load(f)

#optimization statistics
original_entities = 0
relevant_entities = 0

report =[]

# Iterate through the optimized records
for record in optimized_records:
    original_entities += len(record.get("about", []))
    relevant_entities += len(record.get("relevant_about", []))
    relevant_entities_gemini += len(record.get("relevant_about_gemini", []))
    report.append({
        "title": record.get("name", ""),
        "abstracts": record.get("description", ""),
        "program": record.get("program", ""),
        "degree": record.get("degree", ""),
        "original_entities": len(record.get("about", [])),
        "relevant_entities": len(record.get("relevant_about", [])),
        "relevant_entities Gemini": len(record.get("relevant_about_gemini", []))

    }) 

# Print the optimization statistics
print(f"Total original entities: {original_entities}") 
print(f"Total relevant entities: {relevant_entities}")
print(f"Total relevant entities Gemini: {relevant_entities_gemini}")
print(f"Relevancy ratio: {relevant_entities/original_entities:.2%}")
print(f"Relevancy ratio (Gemini): {relevant_entities_gemini/original_entities:.2%}")
# Save the report to a JSON file
with open("optimization_report.json", "w", encoding='utf-8') as f:
    json.dump(report, f, indent=4, ensure_ascii=False)
