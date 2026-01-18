<?php
require 'GraphDB.php';

class Wikidata extends GraphDB{

    public function __construct(){
        GraphDB::__construct();
    }

    function getSibligs($Qcode){
        $sparql="
        SELECT DISTINCT ?relatedItem ?relatedItemLabel ?relatedItemDescription  WHERE {
            { #1.instance of 
                wd:$Qcode wdt:P31 ?instanceOfClass . 
                ?relatedItem wdt:P31 ?instanceOfClass .
            } UNION { 
                # part of
                 wd:$Qcode wdt:P361 ?partOfclass . 
                ?relatedItem wdt:P361 ?partOfclass .
            } UNION { 
                # subclass of
                 wd:$Qcode wdt:P279 ?subclassOfclass . 
                ?relatedItem wdt:P279 ?subclassOfclass .
            }
            
            # 3. Exclude the original item
            FILTER(?relatedItem != wd:$Qcode)
            
            SERVICE wikibase:label { bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }
            }
            LIMIT 100
        ";

        $this->query($sparql,$endpoint='wikidata');

    }

    function getByInstanceOf($Qcode){
        $sparql="
        SELECT DISTINCT ?relatedItem ?relatedItemLabel ?relatedItemDescription  WHERE {
            
            ?relatedItem wdt:P31 wd:$Qcode .
             
            # 3. Exclude the original item
            FILTER(?relatedItem != wd:$Qcode)
            
            SERVICE wikibase:label { bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }
            }
            LIMIT 100
        ";

        $this->query($sparql,$endpoint='wikidata');
    }

    function getByPartOf($Qcode){
        $sparql="
        SELECT DISTINCT ?relatedItem ?relatedItemLabel ?relatedItemDescription  WHERE {
            # part of
            ?relatedItem wdt:P361 wd:$Qcode .
             
            # 3. Exclude the original item
            FILTER(?relatedItem != wd:$Qcode)
            
            SERVICE wikibase:label { bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }
            }
            LIMIT 100
        ";

        $this->query($sparql,$endpoint='wikidata');
    }

    function getBysubclassOf($Qcode){
        $sparql="
        SELECT DISTINCT ?relatedItem ?relatedItemLabel ?relatedItemDescription  WHERE {
            # subclass of
            ?relatedItem wdt:P279 wd:$Qcode .
             
            # 3. Exclude the original item
            FILTER(?relatedItem != wd:$Qcode)
            
            SERVICE wikibase:label { bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }
            }
            LIMIT 100
        ";

        $this->query($sparql,$endpoint='wikidata');
    }
    
    function getSuperClasses($Qcode){
        $sparql="
        SELECT DISTINCT ?subclassOfclass ?subclassOfclassLabel ?partOfclass ?partOfclassLabel ?instanceOfClass ?instanceOfClassLabel  WHERE {
            {wd:$Qcode wdt:P279 ?subclassOfclass .
            } UNION
            {wd:$Qcode wdt:P361 ?partOfclass . 
            } UNION
            {wd:$Qcode wdt:P31 ?instanceOfClass . 
            }
                   
            SERVICE wikibase:label { bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }
            }
            LIMIT 20
        ";

        $this->query($sparql,$endpoint='wikidata');
    }
}