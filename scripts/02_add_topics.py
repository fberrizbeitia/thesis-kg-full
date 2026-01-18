
import spacy
import json
from spacy.pipeline.entity_linker import DEFAULT_NEL_MODEL

#load records
with open("records.json", "r", encoding='utf-8') as f:
    records = json.load(f)

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Add the EntityLinker to the pipeline
nlp.add_pipe("entityLinker", last=True)

linked_records = []

for record in records:
    # Set the abstract for the current record
    print(record['ID'])
    abstract = record.get("description", "")
    
    # Skip if no abstract is provided
    if not abstract:
        continue
    
    # Process the abstract with spaCy
    doc = nlp(abstract)
    
    # Access all linked entities in the document
    all_linked_entities = doc._.linkedEntities
    
    # Deduplicate entities
    control = set()
    entities = []
    cont = 1
    for entity in all_linked_entities:
        if entity.get_url() not in control:
            control.add(entity.get_url())
            new_entity = {
                "ID": cont,
                "label": entity.get_label(),
                "uri": entity.get_url(),
                "description": entity.get_description()
            }
            entities.append(new_entity)
            cont += 1
    
    # Add the entities to the record
    record["about"] = entities
    linked_records.append(record)

# Save the linked records to a JSON file
with open("linked_records.json", "w", encoding='utf-8') as f:
    json.dump(linked_records, f, indent=4, ensure_ascii=False)

