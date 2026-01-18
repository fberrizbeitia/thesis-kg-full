<?php
require_once "../Model/Person.php";
$objPerson = new Person();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);


$objPerson->getAdvisorByTopic($json_data);
$jsonString = $objPerson->getJson();

header('Content-Type: application/json'); // Set header for browser display
echo $jsonString;
?>