import sys
import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, SPARQLStore
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF, OWL

BLAZEGRAPH_SPARQL_ENDPOINT = "http://localhost:9999/blazegraph/sparql"
store_for_query = SPARQLStore(query_endpoint=BLAZEGRAPH_SPARQL_ENDPOINT)

def theses_about(wikidata_url):
    sparql = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX schema: <https://schema.org/>
        SELECT ?id ?title ?description
            WHERE {{
                ?thesis schema:name ?title.
              	?thesis schema:description ?description.
                ?thesis schema:identifier ?id.
                ?thesis schema:about <{wikidata_url}>
            }}
        """
    print(sparql)

    results = store_for_query.query(sparql)
    
    if results:
        for row in results:
            print(f"""
                  ID: {row.id}, 
                  Title: {row.title}
                  Abstracrt: {row.description}
            """),
    else:
        print("No results found.")


def show_help():
    print(f"""
    ------------------------------------------------------
    USAGE
    -----------------------------------------------
    theses_about: <wikidata_qualifier>
    authors_about: <wikidata_qualifier>
    advisors_about: <wikidata_qualifier>
    
    exit
    """)


def main():
    print("Thesis graph CLI interface")
    while True:
        choice = input()

        if choice == "help":
            show_help()
        elif choice == "theses_about":
            wikidata_url = input("insert wikidata URL: ")
            theses_about(wikidata_url)
        elif choice == "exit":
            sys.exit()
        else:
            print ("wrong command write help for options")


if __name__ == "__main__":
    main()