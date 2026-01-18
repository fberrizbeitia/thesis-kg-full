<?php
require 'GraphDB.php';

class Person extends GraphDB{

    public function __construct(){
        GraphDB::__construct();
    }

     function getAuthorsByTopic($wikidata_urls){
        $topicPattern = $this->createAboutPattern($wikidata_urls);
        $sparql=
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
         PREFIX schema: <https://schema.org/>
         PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

         SELECT DISTINCT ?identifier ?familyName ?givenName ?program 
            WHERE {
                $topicPattern 
              	?thesis thesis:program ?program.
                ?thesis schema:author  ?author.
                ?author schema:identifier ?identifier.
                ?author schema:familyName ?familyName.
              	?author schema:givenName ?givenName
         }";
         $this->query($sparql);
    }

    function getAdvisorByTopic($wikidata_urls){
        $topicPattern = $this->createAboutPattern($wikidata_urls);
        $sparql=
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
         PREFIX schema: <https://schema.org/>
         PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

         SELECT DISTINCT ?identifier ?familyName ?givenName ?program 
            WHERE {
                $topicPattern 
              	?thesis thesis:program ?program.
                ?thesis thesis:advisor  ?advisor.
                ?advisor schema:identifier ?identifier.
                ?advisor schema:familyName ?familyName.
              	?advisor schema:givenName ?givenName
         }";
         $this->query($sparql);
    }

    function getAuthorByThesis($thesisID){
        $sparql="
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX schema: <https://schema.org/>
        PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

        SELECT DISTINCT ?identifier ?familyName ?givenName ?program 
            WHERE {
                    ?thesis schema:identifier \"$thesisID\".	
                    ?thesis thesis:program ?program.
                    ?thesis schema:author  ?author.
                    ?author schema:identifier ?identifier.	
                    ?author schema:familyName ?familyName.
                    ?author schema:givenName ?givenName
            }
        ";
        $this->query($sparql);
    }

    function getAuthorFromAdvisor($advisorID){
        $sparql="
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT DISTINCT ?identifier ?familyName ?givenName
                WHERE {
                        ?thesis thesis:advisor ?advisor.
                        ?advisor schema:identifier \"$advisorID\".
                        ?thesis schema:author  ?author.
                        ?author schema:identifier ?identifier.	
                        ?author schema:familyName ?familyName.
                        ?author schema:givenName ?givenName
                }
        ";
        $this->query($sparql);
    }

    function getAdvisorByThesis($thesisID){
        $sparql="
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX schema: <https://schema.org/>
        PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

        SELECT DISTINCT ?identifier ?familyName ?givenName ?program 
            WHERE {
                    ?thesis schema:identifier \"$thesisID\".	
                    ?thesis thesis:program ?program.
                    ?thesis thesis:advisor  ?advisor.
                    ?advisor schema:identifier ?identifier.	
                    ?advisor schema:familyName ?familyName.
                    ?advisor schema:givenName ?givenName
            }
        ";
        $this->query($sparql);
    }

    function getAdvisorByAuthor($authorID){
        $sparql="
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT ?identifier ?familyName ?givenName
                WHERE {
                    
                    ?thesis schema:author ?author.
                  	?author schema:identifier \"$authorID\".
                    ?thesis thesis:advisor  ?advisor.
                  	?advisor schema:identifier ?identifier.	
                    ?advisor schema:familyName ?familyName.
                    ?advisor schema:givenName ?givenName
                  
                }
        ";

        $this->query($sparql);
    }

}

?>