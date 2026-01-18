<?php
require_once '../Model/Wikidata.php';
$objWD = new Wikidata();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);


$objWD->getSuperClasses($json_data) ;
  
$json_string = $objWD->getJson();  

header('Content-Type: application/json'); // Set header for browser display
echo $json_string;

?>