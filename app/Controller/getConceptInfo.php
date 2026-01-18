<?php
require_once '../Model/Concept.php';
$objConcept = new Concept();
$info = $objConcept->getOgInfo('https://www.wikidata.org/wiki/Q1121708');

header('Content-Type: application/json'); // Set header for browser display
echo json_encode($info);

?>