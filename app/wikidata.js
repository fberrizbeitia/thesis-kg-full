const searchInput = document.getElementById('search-bar');
const suggestionsList = document.getElementById('suggestions');
let timeout = null;

searchInput.addEventListener('input', () => {
    clearTimeout(timeout);
    const query = searchInput.value;

    if (query.length < 2) {
        suggestionsList.innerHTML = '';
        return;
    }

    // Debounce to prevent too many API calls
    timeout = setTimeout(() => {
        fetchQualifiers(query);
    }, 300);
});

async function fetchQualifiers(query) {
    const url = `https://www.wikidata.org/w/api.php?action=wbsearchentities&search=${query}&language=en&format=json&origin=*`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        displaySuggestions(data.search);
    } catch (error) {
        console.error("API Error:", error);
    }
}

function displaySuggestions(results) {
    suggestionsList.innerHTML = '';
    results.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${item.label} (${item.id})</strong><br>
            <span class="desc">${item.description || 'No description available'}</span>
        `;
        //li.onclick = () => selectItem(item);
        li.onclick = () => addConcept(item,"concepts-list");
        suggestionsList.appendChild(li);
    });

}

function removeConcept(id){
    var elem = document.getElementById("concept-"+id);
    elem.remove();
    var elemExpansion = document.getElementById("expansion-"+id);
    elemExpansion.remove();
}

function addConcept(item,containerID) {

    suggestionsList.innerHTML = '';
    if (item.id !== undefined){
        if(item.id.includes("www.wikidata.org/entity")){
            wikidataURL = item.id;
        }else{
            wikidataURL = "http://www.wikidata.org/entity/"+item.id;
        }
              
        id = (Math.random() * 1000)
        id = Math.round(id);

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = id;
        checkbox.name = 'option_' + id; // Give it a name for form submission
        checkbox.value = wikidataURL;
        checkbox.checked = true; 


        var label = document.createElement('a');
        label.href = wikidataURL;
        label.target = "_blank";
        label.textContent = item.label + ": "+ item.description;

        var removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remove';
        removeBtn.setAttribute('onclick',"removeConcept("+id+")")

        var expandBtn = document.createElement('button');
        expandBtn.textContent = 'Expand';
        expandBtn.setAttribute('onclick',"expandElement('"+item.id+"',"+id+")");

        var expansion = document.createElement("div");
        expansion.id =  "expansion-"+id;
        expansion.classList.add("expansion");


        var row = document.createElement('div');
        row.id = "concept-"+id;
        row.append(checkbox);
        row.append(label);
        row.append(expandBtn);
        row.append(removeBtn);

        document.getElementById(containerID).append(row);
        document.getElementById(containerID).append(expansion);

    }
}

function addSuperClassEntity(item,containerID,expandCall){
    
    id = (Math.random() * 1000)
    id = Math.round(id);

    var label = document.createElement('a');
    label.href = item.id;
    label.target = "_blank";
    label.textContent = item.label;

    var expandBtn = document.createElement('button');
    expandBtn.textContent = 'Add Concepts';
    expandBtn.setAttribute('onclick',expandCall+"('"+item.id+"')");

    var row = document.createElement('div');
        row.id = "superClass-"+id;
        row.classList.add("classrow");
        row.append(label);
        row.append(expandBtn);
    

    document.getElementById(containerID).append(row);
}

function displaySuperClass(array,title,id,expandCall){

    if(array.length > 0){
        var classID = (Math.random() * 1000);
        classID = Math.round(classID);

        var instanceOfElement = document.createElement("div");
        instanceOfElementID = "class-section-"+classID;
        instanceOfElement.id = instanceOfElementID;
        instanceOfElement.classList.add("classSection");
        var instanceOfTitle = document.createElement("h4");
        instanceOfTitle.textContent = title;
        instanceOfElement.append(instanceOfTitle);
        document.getElementById("expansion-"+id).append(instanceOfElement);
        array.forEach(item =>{
            addSuperClassEntity(item,instanceOfElementID,expandCall);
        });
    }
    
}


async function expandElement(qcode,elementID){
    controllerURL = "Controller/getWikidataSuper.php";
    var json_result = await wikidataControllerCall(qcode,controllerURL);

    var instanceOfarray = [];
    var partOfarray = [];
    var subclasOfarray = [];

    json_result.forEach(record => {
        if(record.subclassOfclass != ""){
            var elem = {
                "id": record.subclassOfclass,
                "label": record.subclassOfclassLabel,
                "description":""
            };
            subclasOfarray.push(elem)
        }else{
            if(record.partOfclass != ""){
                var elem = {
                    "id": record.partOfclass,
                    "label": record.partOfclassLabel,
                    "description":""
                };
                partOfarray.push(elem);
            }else{
                var elem = {
                    "id": record.instanceOfClass,
                    "label": record.instanceOfClassLabel,
                    "description":""
                };
                instanceOfarray.push(elem);
            }
        }
    });

   displaySuperClass(instanceOfarray,"Instance of:",elementID,"expandByInstanceOf");
   displaySuperClass(partOfarray,"Part of:",elementID,"expandByPartOf");
   displaySuperClass(subclasOfarray,"Subclass of:",elementID,"expandBySubclassOf");
    
}


function getqcode(wikidataURL){
    const parts = wikidataURL.split("/");
    return (parts.at(-1));
}

async function expandByInstanceOf(wikidataURL){
    const qcode = getqcode(wikidataURL)
    const controllerURL = "Controller/getWikidataSibligs.php";
    params = {
        "qcode":qcode,
        "expand":"instanceOf"
    }

    json_result = await wikidataControllerCall(params,controllerURL);
    wikidataDisplayResults(json_result,"concepts-list");
}

async function expandByPartOf(wikidataURL){
    const qcode = getqcode(wikidataURL)
    const controllerURL = "Controller/getWikidataSibligs.php";
    params = {
        "qcode":qcode,
        "expand":"partOf"
    }

    json_result = await wikidataControllerCall(params,controllerURL);
    wikidataDisplayResults(json_result,"concepts-list");
}

async function expandBySubclassOf(wikidataURL){
    const qcode = getqcode(wikidataURL)
    const controllerURL = "Controller/getWikidataSibligs.php";
    params = {
        "qcode":qcode,
        "expand":"subclassOf"
    }

    json_result = await wikidataControllerCall(params,controllerURL);
    wikidataDisplayResults(json_result,"concepts-list");
}


function wikidataDisplayResults(json_data,containerID){

    
    
    json_data.forEach(record => {
        var parts = record.relatedItem.split("/");
        var item = {
            "id":parts.at(-1),
            "label":record.relatedItemLabel,
            "description":record.relatedItemDescription
        }
        addConcept(item,containerID);
    });
}


async function wikidataControllerCall(params,controllerURL){

    json_params = JSON.stringify(params)
    console.log(json_params);
    const response = await fetch(controllerURL, {
            method: 'POST', // Specify the HTTP method as POST
            headers: {
                'Content-Type': 'application/json', // Indicate that we are sending JSON data
                'Accept': 'application/json' // Indicate that we prefer JSON in response
            },
            body:  json_params
        })
    
    const json_result = await response.json();
    return(json_result);
}