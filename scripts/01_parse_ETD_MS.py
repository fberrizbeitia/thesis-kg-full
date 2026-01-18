import xmltodict
import json
import os 

def load_xml_as_dict(file_path):
    """
    Loads an XML file using xmltodict and returns a dictionary representation.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_string = f.read()
            data_dict = xmltodict.parse(xml_string)
        return data_dict
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e: # Catch xmltodict parsing errors
        print(f"Error parsing XML file with xmltodict: {e}")
        return None

def parse_person(person_str):
    if(isinstance(person_str,dict)):
        person_array = person_str['#text'].split(',')
    else:
        person_array = person_str.split(',')
    person = {
        "givenName": person_array[1],
        "familyName": person_array[0]
    }
    return person

def parse_persons(persons):
    result = []
    if(isinstance(persons,list)):
        for individual in persons:
            person = parse_person(individual)
            result.append(person)
    else:
        person = parse_person(persons)
        result.append(person)
    return result


def parse_etd_ms(filePath):
    xml_dict = load_xml_as_dict(filePath)
    entities = []
    for thesis in xml_dict['collection']['etd_ms:thesis']:

        print(thesis['etd_ms:title'])

        identifiers = thesis['etd_ms:identifier']
        eprintID = identifiers[0].split('-')[2]
        url = "https://spectrum.library.concordia.ca/id/eprint/"+eprintID

        

        authors = parse_persons(thesis['etd_ms:creator'])
        advisors = parse_persons(thesis["etd_ms:contributor"])
        
        entity = {
            'ID': eprintID,
            'name': thesis['etd_ms:title'],
            'url': url,
            'description': thesis['etd_ms:description'],
            'datePublished': thesis['etd_ms:date'],
            'creators': authors,
            'advisors': advisors,
            'program': thesis['etd_ms:degree']['etd_ms:discipline'],
            'degree':thesis['etd_ms:degree']['etd_ms:name']
        }
        entities.append(entity)
    return entities


def flatten_list(nested_list):
    flattened_list = []
    for sublist in nested_list:
        for item in sublist:
            flattened_list.append(item)
    return(flattened_list)


#read all the xml files on tje etd_ms directory
full_parsed_dataset = []
for fileName in os.listdir('etd_ms'):
    filePath = 'etd_ms/'+fileName
    parsed_file = parse_etd_ms(filePath)
    full_parsed_dataset.append(parsed_file)

flatten_dataset = flatten_list(full_parsed_dataset)
# Save the entities to a JSON file
with open("records.json", "w", encoding='utf-8') as f:
    json.dump(flatten_dataset, f, indent=4, ensure_ascii=False)




