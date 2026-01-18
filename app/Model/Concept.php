<?php
require 'GraphDB.php';

class Concept extends GraphDB{

    public function __construct(){
        GraphDB::__construct();
    }

    public function getCoConcepts($wikidata_urls){
        $topicPattern = $this->createAboutPattern($wikidata_urls);

        $sparql="
        
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT ?concept ?title  ?description (COUNT(?concept) AS ?count)
            WHERE{
                $topicPattern 
                ?thesis schema:about ?concept.
                ?concept schema:name ?title.
                ?concept schema:description ?description
            }
            GROUP BY ?concept ?title ?description
            ORDER BY DESC (?count)
        ";
       // echo ($sparql);
        $this->query($sparql);
    }

    public function getLabel($wikidataURL){
        $wikidataArray = explode("/",$wikidataURL);
        $qcode = end($wikidataArray);
        $sparql ="
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX wd: <http://www.wikidata.org/entity/>

            SELECT ?label
            WHERE
            {
            wd:".$qcode." rdfs:label ?label.
            FILTER(LANG(?label)='en')
            }
        ";
        
        $this->query($sparql,'wikidata');

    }

    function curl($url){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36');
        $response = curl_exec($ch);
        curl_close($ch);
        return($response);
        
    }


    function getOgInfo($wikidataURL){
        $result = [];
        $pageHTML = $this->curl($wikidataURL);
        $doc = new DOMDocument();
        @$doc->loadHTML($pageHTML);
        $metatags = $doc->getElementsByTagName('meta');
         
        foreach($metatags as $metatag){
            $property = $metatag->getAttribute('property');
          //  var_dump($property);
            if($property == "og:title"){
                $result['label'] = $metatag->getAttribute('content');
            }
            if($property == "og:description"){
                $result['description'] = $metatag->getAttribute('content');
            }
        }
       return($result);
       
    }

    function getByThesis($thesisID){
           $sparql="
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT DISTINCT ?wikidataURL ?title ?description
                WHERE {
                    ?thesis schema:identifier \"$thesisID\".
                    ?thesis schema:about ?concept.
                    ?concept schema:url ?wikidataURL.
                    ?concept schema:name ?title.
                    ?concept schema:description ?description
                }
           "; 

           $this->query($sparql);

          // echo($sparql);
    }

    function getByAuthor($authorID){
        $sparql="
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT DISTINCT ?wikidataURL ?title ?description
                WHERE {
                    ?thesis schema:author ?author.
                    ?author schema:identifier \"$authorID\".
                    ?thesis schema:about ?concept.
                    ?concept schema:url ?wikidataURL.
                    ?concept schema:name ?title.
                    ?concept schema:description ?description
                    
}
        ";
        $this->query($sparql);
    }

    function getByAdvisor($advisorID){
        $sparql="
            PREFIX schema: <https://schema.org/>
            PREFIX thesis: <http://www.semanticweb.org/fberrizb/ontologies/2025/5/thesis/>

            SELECT DISTINCT ?wikidataURL ?title ?description
                WHERE {
                    ?thesis thesis:advisor ?advisor.
                    ?advisor schema:identifier \"$advisorID\".
                    ?thesis schema:about ?concept.
                    ?concept schema:url ?wikidataURL.
                    ?concept schema:name ?title.
                    ?concept schema:description ?description
                    
}
        ";
        $this->query($sparql);
    }

 
}


?>