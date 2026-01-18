<?php
require_once '../Model/Concept.php';
$objConcept = new Concept();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);

$objConcept->getCoConcepts($json_data);
$json_string = $objConcept->getJson();

$concepts = json_decode($json_string,true);

/*
$concept_with_labels = [];
$i = 0;

foreach ($concepts as $concept){
    if($i < 10){
        $objConcept->getLabel($concept['url']);
        $labeljson = json_decode($objConcept->getJson(),true);
        
    
        $concept['label'] = $labeljson[0]['label'];
        $i++;
    }
    
    $concept_with_labels[] = $concept;
}
*/

header('Content-Type: application/json'); // Set header for browser display
echo json_encode($concepts);
?>