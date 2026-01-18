<?php
ini_set('display_errors', '0');
ini_set('log_errors', '1');
ini_set('error_log', '../error.log');
require_once '../vendor/autoload.php';

class GraphDB{

    private $sparqlQueryEndpoint = 'http://localhost:9999/blazegraph/sparql'; 
    private $wikidataEnpoint = 'https://query.wikidata.org/sparql';
    public $sparqlClient;
    public $wikidataClient;
    public $results;
    public $resultsTotal = 0;
    public $errorMgs = "";

    public function __construct(){
        $this->sparqlClient = new EasyRdf\Sparql\Client($this->sparqlQueryEndpoint);
        $this->wikidataClient = new EasyRdf\Sparql\Client($this->wikidataEnpoint);
    }

    public function query($sparqlQueryString,$endpoint='local'){
        error_log($sparqlQueryString);
        try {
            if($endpoint == 'local'){
                $this->results = $this->sparqlClient->query($sparqlQueryString);
            }else{
                $this->results = $this->wikidataClient->query($sparqlQueryString);
            }
            
            $this->resultsTotal = $this->results->count();
            $this->errorMgs = "";
            return true;
        } catch (Exception $e) {
            $this->errorMgs = $e->getMessage();
            error_log("Wikidata Error: " . $this->errorMgs);
            return false;

        }
    }

    public function getJson(){
        $resultsArray = [];

        if($this->resultsTotal > 0){

            $fields = $this->results->getFields();
            foreach($this->results as $result){
                $row = [];
                foreach($fields as $field){
                    if(isset($result->$field)) {
                        $value = $result->$field->__toString() ;
                        $row[$field] = $value;
                    }else{
                        $row[$field] = "";
                    }
                }
                $resultsArray[] = $row;
            }
        }else{
            $resultsArray[] = array("message"=> "No results were found");
        }

        // Convert the PHP array to a JSON string
        $jsonString = json_encode($resultsArray, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
        
        return $jsonString;
       
    }

    private function ensureHttps($url) {
        $secureUrl = str_replace("http:", "https:", $url);
        $formated = str_replace("entity/", "wiki/", $secureUrl);
        return $formated;
    }

    public function createAboutPattern($wikidata_url_array){
        $aboutPattern = "";
        if(is_array($wikidata_url_array)){
            foreach($wikidata_url_array as $concept){
                $aboutPattern .= "<".$this->ensureHttps($concept).">";
            }
        }else{
            $aboutPattern .= "<".$this->ensureHttps($wikidata_url_array).">";
        }

        $sparqlSnippent = "VALUES ?topic { $aboutPattern }
                            ?thesis schema:about ?topic .
                        ";
        return $sparqlSnippent;
        
    }
        
}




?>