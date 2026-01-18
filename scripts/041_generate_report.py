import json
import csv
from collections import defaultdict

# 1. Load the optimized records
input_file = "optimized_records_gemini.json"
try:
    with open(input_file, "r", encoding='utf-8') as f:
        records = json.load(f)
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    records = []

# 2. Process and Aggregate Data
stats = defaultdict(lambda: defaultdict(lambda: {"orig": 0, "rel": 0, "rel_gemini":0, "count": 0}))

for r in records:
    p = r.get("program", "Unknown Program")
    d = r.get("degree", "Unknown Degree")
    
    # FIX: These are the actual keys from your JSON sample
    # We use .get() to find the list, and default to an empty list [] if not found
    orig_list = r.get("about", []) 
    rel_list = r.get("relevant_about", [])
    rel_list_gemini = r.get("relevant_about_gemini", [])
    

    # Count the items in the lists
    o_count = len(orig_list) if isinstance(orig_list, list) else 0
    r_count = len(rel_list) if isinstance(rel_list, list) else 0
    r_count_gemini = len(rel_list_gemini) if isinstance(rel_list_gemini, list) else 0
    
    stats[p][d]["orig"] += o_count
    stats[p][d]["rel"] += r_count
    stats[p][d]["rel_gemini"] += r_count_gemini
    stats[p][d]["count"] += 1

# 3. Prepare data for CSV export
rows = []
for program, degrees in stats.items():
    for degree, data in degrees.items():
        ratio = (data["rel"] / data["orig"]) if data["orig"] > 0 else 0
        ratio_gemini = (data["rel_gemini"] / data["orig"]) if data["orig"] > 0 else 0
        rows.append({
            "Program": program,
            "Degree": degree,
            "Total Records": data["count"],
            "Original Entities Total": data["orig"],
            "Relevant Entities Total (Gemma3:4b)": data["rel"],
            "Relevant Entities (Gemini) Total": data["rel_gemini"],
            "Relevancy Ratio (Gemma3:4b)": f"{ratio:.2%}",
            "Relevancy Ratio (Gemini)": f"{ratio_gemini:.2%}",
        })

# 4. Export to CSV
csv_file = "optimization_summary.csv"
if rows:
    with open(csv_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# 5. Export to JSON
json_report = []
for p, degrees in stats.items():
    p_data = {"program": p, "degree_stats": []}
    for d, data in degrees.items():
        ratio = (data["rel"] / data["orig"]) if data["orig"] > 0 else 0
        p_data["degree_stats"].append({
            "degree": d,
            "metrics": {
                "records": data["count"],
                "original": data["orig"],
                "relevant (Gemma3)": data["rel"],
                "relevant (Gemini)": data["rel_gemini"],
                "ratio (Gemma3)": f"{ratio:.2%}",
                "ratio (Gemini)": f"{ratio:.2%}"
            }
        })
    json_report.append(p_data)

with open("optimization_report.json", "w", encoding='utf-8') as f:
    json.dump(json_report, f, indent=4, ensure_ascii=False)

print(f"Success! Processed {len(records)} records.")
print(f"Files created: '{csv_file}' and 'optimization_report.json'")