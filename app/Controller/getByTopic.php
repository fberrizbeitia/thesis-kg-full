<?php
require_once "../Model/Thesis.php";
$objThesis = new Thesis();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);


$objThesis->getByTopic($json_data);
$jsonString = $objThesis->getJson();

header('Content-Type: application/json'); // Set header for browser display
echo $jsonString;

?>