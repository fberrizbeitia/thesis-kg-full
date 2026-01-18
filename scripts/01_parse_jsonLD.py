import json

def load_jsonld(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Example usage:
jsonld_dict = load_jsonld('2025.json')

graph = jsonld_dict.get('@graph', [])
entities = []
for item in graph:
    url = item.get('url').split('/')
    id = url[-2]

    entity = {
        'ID': id,
        'name': item.get('name'),
        'url': item.get('url'),
        'description': item.get('description', ''),
        'datePublished': item.get('datePublished', ''),
        'creator': item.get('creator', ''),
        'keywords': item.get('keywords', [])
    }
    entities.append(entity)


# Save the entities to a JSON file
with open("records.json", "w", encoding='utf-8') as f:
    json.dump(entities, f, indent=4, ensure_ascii=False)




