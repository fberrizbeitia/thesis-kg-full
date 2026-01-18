<?php
require 'GraphDB.php';

class Thesis extends GraphDB{
    public $title;
    public $abstract;
    public $publicationDate;
    public $authors;
    public $advisors;
    public $topics;

    public function __construct(){
        GraphDB::__construct();
    }

    
    function getByTopic($wikidata_urls){

        $topicPattern = $this->createAboutPattern($wikidata_urls);

        $sparql = "
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/> 

            SELECT DISTINCT ?identifier ?title ?description ?program 
            WHERE {
                
                $topicPattern
                
                # Fetch details
                ?thesis schema:name ?title .
                ?thesis schema:description ?description .
                ?thesis schema:identifier ?identifier .
                ?thesis thesis:program ?program .
            }
        ";

        $this->query($sparql);
    }



    function getProgramsByTopic($wikidata_urls){
        $topicPattern = $this->createAboutPattern($wikidata_urls);
        $sparql = 
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
         PREFIX schema: <https://schema.org/>
         PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/> 
         SELECT DISTINCT (count(?id) AS ?numberOfTheses)  ?identifier
            WHERE {
                $topicPattern
        
                ?thesis schema:identifier ?id.
				?thesis thesis:program ?identifier.
                
            }
        GROUP BY ?identifier 
        ORDER BY DESC(?numberOfTheses) ?identifier ";

        $this->query($sparql);
    }

    function getByProgram($program_name){
        $sparql="
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT ?identifier ?title ?description ?author ?advisor
                WHERE {
                    ?thesis schema:identifier ?identifier.
                    ?thesis schema:name ?title.
                    ?thesis schema:description ?description.
                    ?thesis schema:identifier ?program.
                    ?thesis schema:author ?author.
                  	?thesis thesis:advisor ?advisor.
                  	?thesis thesis:program \"$program_name\".
                }
        
        ";
        $this->query($sparql);
    }

    function getByAdvisor($advisorID){
        $sparql = "
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT ?identifier ?title ?description ?program 
                WHERE {
                    ?thesis schema:name ?title.
                    ?thesis schema:description ?description.
                    ?thesis schema:identifier ?identifier.
                    ?thesis thesis:program ?program.
                    ?thesis thesis:advisor ?advisor.
                    ?advisor schema:identifier \"$advisorID\"	
                }
        ";

        $this->query($sparql);
    }

    function getByAuthor($authorID){
        $sparql = "
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT ?identifier ?title ?description ?program 
                WHERE {
                    ?thesis schema:name ?title.
                    ?thesis schema:description ?description.
                    ?thesis schema:identifier ?identifier.
                    ?thesis thesis:program ?program.
                    ?thesis schema:author ?author.
                    ?author schema:identifier \"$authorID\"	
                }
        ";

        $this->query($sparql);
    }

    

   

}


?>