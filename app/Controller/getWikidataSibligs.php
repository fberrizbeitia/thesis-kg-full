<?php
require_once '../Model/Wikidata.php';
$objWD = new Wikidata();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);


//var_dump($json_data);

if($json_data["expand"] == "all"){
    $objWD->getSibligs($json_data["qcode"]);
}elseif($json_data["expand"] == "instanceOf"){
    $objWD->getByInstanceOf($json_data["qcode"]);
}elseif($json_data["expand"] == "partOf"){
    $objWD->getByPartOf($json_data["qcode"]);
}elseif($json_data["expand"] == "subclassOf"){
    $objWD->getBysubclassOf($json_data["qcode"]);
}
   

$json_string = $objWD->getJson();  


header('Content-Type: application/json'); // Set header for browser display
echo $json_string;

?>