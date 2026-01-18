#load linked_records.json
import json
from ollama import generate

# Load linked records
with open("linked_records.json", "r", encoding='utf-8') as f:
    linked_records = json.load(f)

optimized_records = []

instruction = "You are an expert in evaluating the relevance of topics to abstracts. For each entity, determine if the description of the entity is relevant to the topic of the abstract. Be very strict. Respond with 'yes' or 'no'. Provide your answer in JSON format as follows: {'relevant': 'yes' or 'no'}.\n\n"

instruction2 = "You are a strict relevance evaluator. For each 'entity description' provided, determine if it is directly relevant to the 'abstract'. Respond ONLY with 'yes' or 'no' in JSON format. Format:{'relevant': 'yes'} or {'relevant': 'no'}"

for record in linked_records:
    abstract = record.get("description", "")
    if not abstract:
        continue  # Skip records without an abstract
    entities = record.get("about", [])
    relevant_entities = []
    print(f"Processing record with title: {record.get('name','') }")  
    for entity in entities:
        print(".",end="")  
        entity_json = json.dumps(entity)
        promptTxt = instruction2 + "\n entity description:" + entity_json + "\n abstract: " + abstract 

        response = generate(
            model="gemma3:4b",
            prompt=promptTxt,   
            format='json',
            stream=False,
            options={'temperature': 0}
        )
        
        # Convert the response to a dictionary
        try:
            responseJson = json.loads(response['response'])
        except json.JSONDecodeError:
            print("Error decoding JSON response. Skipping this entity.")
            continue
        
        if 'relevant' in responseJson:
            # Check if the response is true
            if responseJson['relevant'] == 'yes':
                relevant_entities.append(entity)

    # Add the relevant entities to the record
    if relevant_entities:
        record["relevant_about"] = relevant_entities
    optimized_records.append(record)



# Save the optimized records to a JSON file
with open("optimized_records.json", "w", encoding='utf-8') as f:
    json.dump(optimized_records, f, indent=4, ensure_ascii=False)