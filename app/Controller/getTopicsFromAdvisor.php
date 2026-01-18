<?php
require_once '../Model/Concept.php';
$objConcept = new Concept();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);

$objConcept->getByAdvisor($json_data);
$json_string = $objConcept->getJson();


header('Content-Type: application/json'); // Set header for browser display
echo $json_string;

?>