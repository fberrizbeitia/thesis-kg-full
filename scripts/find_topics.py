
import spacy
import json
from spacy.pipeline.entity_linker import DEFAULT_NEL_MODEL
from ollama import generate


# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Add the EntityLinker to the pipeline
nlp.add_pipe("entityLinker", last=True)


abstract = """This presentation will cover our ongoing work investigating and deploying generative AI technology in the context of libraries and memory institutions. It’s not novel that libraries provide online human or machine-based chat services, but taking advantage of generative AI requires new technical approaches and considerations around the ethics and usefulness of conversational agents. We will discuss our development of a chatbot configured for delivering academic library information services. This includes defining a protocol for assessing and guiding implementation decisions as well as evaluating the tool’s utility.

Our initial step in developing the chatbot involved building a knowledge base (stored on an in-house metadata management system), which could be connected to generative AI technology. Next, we experimented with a variety of open source and proprietary language models to understand how each performs. We are testing the following approaches: A closed source large language model (Bing Chat / Gemini / ChatGPT) prompted to act as reference personnel; a context-aware closed source LLM (OpenAI GPT); and a context-aware open source LLM (Llama). We are testing with questions that a useful chatbot should be able to answer. The chatbot’s responses for each approach are evaluated comparatively.

A key objective of this project is the testing protocol and evaluation framework. Reference questions often require a dynamic conversation, iterating on the direction of inquiry. This makes it challenging to evaluate outputs as merely accurate or inaccurate. Our study builds on Lai (2023) to develop a testing protocol, incorporating multiple dimensions of user interactions. Our protocol will support the interrogation of ethical concerns around these technologies and their application. We are operationalizing aspects of the LC Labs AI Planning Framework (Library of Congress, 2023) to define use cases for generative AI in information services and ethical criteria."""


doc = nlp(abstract)

# Access all linked entities in the document
all_linked_entities = doc._.linkedEntities


#deduplicate entities
control = set()
entities = []
cont = 1
for entity in all_linked_entities:
    if entity.get_url() not in control:
        control.add(entity.get_url())
        new_entity = {"ID":cont,"label": entity.get_label(), "uri": entity.get_url(), "description": entity.get_description()}
        entities.append(new_entity)
        cont += 1


instruction = "You are an expert in evaluating the relevance of topics to abstracts. For each entity, determine if the description of the entity is relevant to the topic of the abstract. Be very strict. Respond with 'yes' or 'no'. Provide your answer in JSON format as follows: {'relevant': 'yes' or 'no'}.\n\n"

relevant_entities = []

for entity in entities:

    entity_json = json.dumps(entity)
    promptTxt = instruction + " entity:" + entity_json  + " abstract: " + abstract 

    response = generate(
        model="qwen2.5:0.5b",
        #model="deepseek-r1:1.5b",
        prompt= promptTxt,   
        format='json',
        stream=False,
        options={'temperature': 0}
    )

     # Print the response
    print(f"Entity: {entity_json}")
    print(f"Response: {response['response']}\n")
   
    #convert the response to a dictionary
    try:
        responseJson = json.loads(response['response'])
    except json.JSONDecodeError:
        print("Error decoding JSON response. Skipping this entity.")
        continue
    # Check if the response is true
    if responseJson['relevant'] == 'yes':
        relevant_entities.append(entity)
        print("This entity is relevant to the abstract.")

    print("------------------------------------------------------\n")

    # log the prompt and response
    with open("log.txt", "a") as f:
        f.write(f"Prompt: {promptTxt}\n")
        f.write(f"Response: {response['response']}\n\n")
        f.write(f"------------------------------------------------------\n\n")

   
    
# Save the entities to a JSON file
with open("relevant_entities.json", "w") as f:
    json.dump(relevant_entities, f, indent=4)

# save all entities to a JSON file
with open("all_entities.json", "w") as f:
    json.dump(entities, f, indent=4)
