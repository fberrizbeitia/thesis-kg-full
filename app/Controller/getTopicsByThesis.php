<?php
require_once '../Model/Concept.php';
$objConcept = new Concept();

//get the json data from the post request
$json_data = json_decode(file_get_contents('php://input'),true);

$objConcept->getByThesis($json_data);
$json_string = $objConcept->getJson();

$concepts = json_decode($json_string,true);

/*
$concept_with_labels = [];
$i = 0;


foreach ($concepts as $concept){
    if($i < 10){
        $info = $objConcept->getOgInfo($concept['wikidataURL']);
        $concept['label'] = $info['label'];
        $concept['description'] = $info['description'];
        $i++;
    }
    
    $concept_with_labels[] = $concept;
}
*/


header('Content-Type: application/json'); // Set header for browser display
//echo json_encode($concept_with_labels);
echo json_encode($concepts);
?>