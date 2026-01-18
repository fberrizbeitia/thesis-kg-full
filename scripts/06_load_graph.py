import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, SPARQLStore
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF, OWL

# --- Configuration ---
BLAZEGRAPH_SPARQL_ENDPOINT = "http://localhost:9999/blazegraph/sparql"
BLAZEGRAPH_UPDATE_ENDPOINT = "http://localhost:9999/blazegraph/sparql" # Often the same
THESES_FILE = "scripts/theses_with_data_gemini.ttl"

theses_graph = Graph()
theses_graph.parse(THESES_FILE,format="turtle")

# --- 2. Load the RDF graph into Blazegraph ---
print(f"Attempting to connect to Blazegraph at {BLAZEGRAPH_SPARQL_ENDPOINT} for updates...")
try:
    store_for_update = SPARQLUpdateStore(
        query_endpoint=BLAZEGRAPH_SPARQL_ENDPOINT,
        update_endpoint=BLAZEGRAPH_UPDATE_ENDPOINT
    )
    
    theses_data = theses_graph.serialize(format='turtle')
    insert_query = f"""
            INSERT DATA {{ {theses_data}  }}
        """
    
    print("Sending INSERT DATA query to Blazegraph...")
    store_for_update.update(insert_query) 

    print("Data loaded successfully into Blazegraph.")

except Exception as e:
    print(f"Error loading data into Blazegraph: {e}")
    print("Please ensure Blazegraph is running and accessible at the specified endpoint.")
    exit()