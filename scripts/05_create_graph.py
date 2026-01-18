from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF, OWL
import json
import os
from datetime import datetime, timezone
import uuid

authors = []
advisors = []
concepts = []

def person_exists(person_lastname, person_givenname,persons_list):
    for person in persons_list:
        if(person['givenName'] == person_givenname and person['familyName'] == person_lastname):
            return person['identifier']
    return False

def create_person(person_lastname, person_givenname, graph):
    unique_id_v4 = uuid.uuid4()
    unique_id_v4_str = str(unique_id_v4)
    person_uri = SCHEMA[unique_id_v4_str]
    graph.add((person_uri, RDF.type, SCHEMA.Person))
    graph.add((person_uri,SCHEMA.identifier,Literal(unique_id_v4_str)))
    graph.add((person_uri,SCHEMA.givenName,Literal(person_givenname)))
    graph.add((person_uri,SCHEMA.familyName,Literal(person_lastname)))
    return person_uri

def concept_exists(concept_url,concept_list):
    for concept in concept_list:
        if concept['url'] == concept_url:
            return concept['identifier']
    return False

def create_concept(url,label,description,graph):
    concept_uri = URIRef(url)
    graph.add((concept_uri, RDF.type, OWL.Thing))
    graph.add((concept_uri,SCHEMA.url,Literal(url)))
    graph.add((concept_uri,SCHEMA.name,Literal(label)))
    graph.add((concept_uri,SCHEMA.description,Literal(description)))
    return concept_uri
              
g = Graph()
#load the ontology definition
g.parse("Thesis-ontology.ttl")
SCHEMA = Namespace('https://schema.org/')
THESIS = Namespace('http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/')
g.bind("schema",SCHEMA)
g.bind("thesis",THESIS)

#load the json file with the metadata
with open("optimized_records_gemini.json", "r", encoding='utf-8') as f:
    records = json.load(f)


#iterate over the recordset
for record in records:
    id= record['ID']
    url = record['url']
    name = record['name']
    abstract = record['description']
    program = record['program']
    date = record['datePublished'].split('-')
    year = int(date[0])
    if (len(date) >= 2):
        month = int(date[1])
    else:
        month = 1
    if(len(date) >= 3):
        day = int(date[2])
    else:
        day = 1
    
    dt_object = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)

    #create a new Thesis
    thesis_uri = THESIS[id]
    g.add((thesis_uri,RDF.type,SCHEMA.Thesis))
    g.add((thesis_uri,SCHEMA.identifier,Literal(id)))
    g.add((thesis_uri,SCHEMA.name,Literal(name)))
    g.add((thesis_uri,SCHEMA.description,Literal(abstract)))
    g.add((thesis_uri,SCHEMA.datePublished,Literal(dt_object, datatype=XSD.dateTime)))
    g.add((thesis_uri,THESIS.program,Literal(program)))
    

    # -------------------    Authors     ---------------------------------------------
    #see if the person already exists, if not create it
    for author in record['creators']:
        author_uri_str = person_exists(author['familyName'],author['givenName'],authors)
        if(author_uri_str != False):
            person_uri = SCHEMA[author_uri_str]
          #  g.add((person_uri, RDF.type, SCHEMA.Person))
        else:
            person_uri = create_person(author['familyName'],author['givenName'],g)
            #create a copy of the person for in-memory processing
            newperson = {}
            newperson['givenName'] = author['givenName']
            newperson['familyName'] = author['familyName']
            newperson['identifier'] = author_uri_str
            authors.append(newperson)
        #add relation to the thesis
        g.add((thesis_uri,SCHEMA.author,person_uri))

    # ------------------ ADVISORS --------------------------------------------------
    for advisor in record['advisors']:
        advisor_uri_str = person_exists(author['familyName'],author['givenName'],advisors)
        if(advisor_uri_str != False):
            person_uri = SCHEMA[advisor_uri_str]
          #  g.add((person_uri, RDF.type, SCHEMA.Person))
        else:
            person_uri = create_person(advisor['familyName'],advisor['givenName'],g)
            #create a copy of the person for in-memory processing
            newperson = {}
            newperson['givenName'] = advisor['givenName']
            newperson['familyName'] = advisor['familyName']
            newperson['identifier'] = advisor_uri_str
            advisors.append(newperson)
        #add relation to the thesis
        g.add((thesis_uri,THESIS.advisor,person_uri))

    
    
    # -------------------    CONCEPTS   ---------------------------------------------
    if 'relevant_about' in record:
        for concept in record['relevant_about_gemini']:
            concept_uri_str = concept_exists(concept['uri'],concepts)
            if concept_uri_str != False:
                concept_uri = URIRef(concept_uri_str)
            else:
                concept_uri = create_concept(concept['uri'],concept['label'],concept['description'],g)
                newConcept = {}
                newConcept['url'] = concept['uri']
                newConcept['identifier'] = concept['uri']
                concepts.append(newConcept)
            g.add((thesis_uri,SCHEMA.about,concept_uri))



# Define the filename and format
output_dir = ""
filename = "theses_with_data_gemini.ttl" # .ttl is standard for Turtle format
file_path = os.path.join(output_dir, filename)

# Save the graph
try:
    g.serialize(destination=file_path, format="turtle")
    print(f"Graph successfully saved to: {file_path}")
except Exception as e:
    print(f"Error saving graph: {e}")