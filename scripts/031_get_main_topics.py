#load linked_records.json
import json
from ollama import generate

# Load linked records
with open("linked_records.json", "r", encoding='utf-8') as f:
    linked_records = json.load(f)

optimized_records = []

for record in linked_records:
    print(record['label'])
    abstract = record.get("description", "")
    entities = json.dumps(record.get("about", []))
    promptTxt = """
    Given this abstract and this list of concepts with descriptions in json format.
    Select the most relevant concepts (up to 10) to the abstract. 
    Generate the response in json format as follows:

    Example:   [ {"label": "woman",
                "uri": "https://www.wikidata.org/wiki/Q467",
                "description": "female adult human"}]
    Abstract :"""+abstract+"list of concepts:"+entities

    promptTxt = """
    To assist with information retrieval and categorization, please extract the **up to 10 most pertinent concepts** from the provided `list of concepts` that accurately reflect the main themes and subjects of the given `Abstract`.

    The `list of concepts` is in JSON format, with each concept containing `label`, `uri`, and `description` fields. Your output should mirror this JSON structure, presenting an array of the selected concepts.

    **Abstract:** ["""+abstract+""""]

    **List of Concepts:** ["""+entities+""""]
    """

    response = generate(
            model="gemma3:4b",
            prompt=promptTxt,   
            format='json',
            stream=False,
            options={'temperature': 0}
        )
    record['top_entities'] = json.loads(response['response'])
    optimized_records.append(record)

# Save the optimized records to a JSON file
with open("optimized_records_main_topics.json", "w", encoding='utf-8') as f:
    json.dump(optimized_records, f, indent=4, ensure_ascii=False)