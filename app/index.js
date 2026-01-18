function displayResults(json_data,resultsContainer,resultEntity){
    resultsContainer.innerHTML = '';

    json_data.forEach(record => {
        
        var newResult = document.getElementById('template-step-result-row').content.cloneNode(true);
        var identifier = "";
        for (const key in record){
            var resultContent = newResult.querySelector(".step-result-content")
            
            var propertyName = document.createElement('b');
            propertyName.innerText = key;
            resultContent.appendChild(propertyName);
            
            var propertyValue = document.createElement('p');
            propertyValue.innerText = record[key];
            

            if(key == 'id' || key == 'url'){
                var link = document.createElement('a');
                if(key == 'id'){
                    link.href = "https://spectrum.library.concordia.ca/id/eprint/"+record[key];
                }else{
                    link.href = record[key];
                }
                
                link.textContent = "View";
                link.target = "_blank";
                propertyValue.append(link);
            }
            //save the record identifier to use in thej button cofiguration to keep brosing
            if(key == "identifier"){
                identifier = record[key];
            }
            
            resultContent.appendChild(propertyValue);
        }

        //configure the buttons
        //determine the type of entity
        var thesesBtn = newResult.querySelector('#theses-btn');
        var authorBtn = newResult.querySelector('#author-btn');
        var advisorBtn = newResult.querySelector('#advisor-btn');
        var programsBtn = newResult.querySelector('#programs-btn');
        var conceptsBtn = newResult.querySelector('#concepts-btn');

        if(resultEntity == "Advisor"){
            thesesBtn.setAttribute("onclick","getThesisFromAdvisor('"+identifier+"')");
            authorBtn.setAttribute("onclick","getAuthorFromAdvisor('"+identifier+"')");
            advisorBtn.remove();
            programsBtn.remove();
            conceptsBtn.setAttribute("onclick","getTopicsFromAdvisor('"+identifier+"')");
        }else if(resultEntity == "Thesis"){
            thesesBtn.remove();
            programsBtn.remove();
            authorBtn.setAttribute("onclick","getAuthorFromThesis('"+identifier+"')");
            advisorBtn.setAttribute("onclick","getAdvisorFromThesis('"+identifier+"')");
            conceptsBtn.setAttribute("onclick","getTopicsFromThesis('"+identifier+"')");

        }else if(resultEntity == "Author"){
            authorBtn.remove();
            programsBtn.remove();
            thesesBtn.setAttribute("onclick","getThesisFromAuthor('"+identifier+"')");
            advisorBtn.setAttribute("onclick","getAdvisorFromAuthor('"+identifier+"')");
            conceptsBtn.setAttribute("onclick","getTopicsFromAuthor('"+identifier+"')");

        }else if(resultEntity == "Concept"){
            thesesBtn.remove();
            authorBtn.remove();
            advisorBtn.remove();
            programsBtn.remove();
            conceptsBtn.remove();
        }else if(resultEntity == "Program"){
            thesesBtn.setAttribute("onclick","getThesisFromProgram('"+identifier+"')");
            authorBtn.remove();
            advisorBtn.remove();
            programsBtn.remove();
            conceptsBtn.remove();
        }
        
        resultsContainer.appendChild(newResult);
        resultsContainer.appendChild(document.createElement('hr'))
    });
    
}

async function controllerCall(params,controllerURL,resultsContainer,resultEntity){

    json_params = JSON.stringify(params)

    const response = await fetch(controllerURL, {
            method: 'POST', // Specify the HTTP method as POST
            headers: {
                'Content-Type': 'application/json', // Indicate that we are sending JSON data
                'Accept': 'application/json' // Indicate that we prefer JSON in response
            },
            body:  json_params
        })
    
    const json_result = await response.json();
    
    displayResults(json_result,resultsContainer,resultEntity); 
    console.log(json_result);
}


function removeElement(id){
    var elem = document.getElementById(id);
    elem.remove();
}

/*
function addConcept() {
    wikidataURL = document.getElementById('wikidataURL').value;
    id = (Math.random() * 1000)
    id = Math.round(id);

    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = id;
    checkbox.name = 'option_' + id; // Give it a name for form submission
    checkbox.value = wikidataURL;
    checkbox.checked = true; 

    var label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = wikidataURL;

    var removeBtn = document.createElement('button');
    removeBtn.textContent = 'X';
    removeBtn.setAttribute('onclick',"removeElement('concept-"+id+"')")

    var row = document.createElement('div');
    row.id = "concept-"+id;
    row.append(checkbox);
    row.append(label);
    row.append(removeBtn);

    document.getElementById("concepts-list").append(row);

}
*/

function createResultContainer(title){
    var template = document.getElementById('template-step-container');
    var container = template.content.cloneNode(true);
    var id = Math.round(Math.random() * 10000);
    
    // Get a reference to the main element *before* appending
    // The first child of the template's content is the element you want to work with.
    var mainElement = container.querySelector('#step-container');

    // Update the ID and other content as before
    mainElement.id = "results-"+id;
    mainElement.querySelector('#step-title').textContent = title;
    var results = mainElement.querySelector('#step-result-container');
    var closeBtn = mainElement.querySelector('#step-close-btn');
    closeBtn.setAttribute("onclick", "removeElement('results-"+id+"')");
    
    // Append the DocumentFragment to the main container
    document.getElementById("main-container").append(container);
    
    // Now, call scrollIntoView() on the specific element
    // which is now part of the document
    mainElement.scrollIntoView({ behavior: 'smooth', inline: 'end' });
    
    return results;
}


function getWikidataURLs(){
    const conceptlist = document.getElementById("concepts-list");
    const checkedConcepts = conceptlist.querySelectorAll('input[type="checkbox"]:checked');
    const wikidataURLs = Array.from(checkedConcepts).map(checkbox => checkbox.value);
    return wikidataURLs;
}

async function thesesByConcept(){
    const controllerURL = "Controller/getByTopic.php";
    var newResultContainer = createResultContainer("Theses");
    controllerCall(getWikidataURLs(),controllerURL,newResultContainer,"Thesis");
}

async function programsByConcept(){
    controllerURL = "Controller/getProgramsByTopic.php";
    var newResultContainer = createResultContainer("Programs");
    controllerCall(getWikidataURLs(),controllerURL,newResultContainer,"Program");
}

async function advisorsByConcept() {
    controllerURL = "Controller/getAdvisorsByTopic.php";
    var newResultContainer = createResultContainer("Advisor");
    controllerCall(getWikidataURLs(),controllerURL,newResultContainer,"Advisor");
}

async function authorsByConcept() {
    controllerURL = "Controller/getAuthorsByTopic.php";
    var newResultContainer = createResultContainer("Authors");
    controllerCall(getWikidataURLs(),controllerURL,newResultContainer,"Author");
}

async function getCoConcepts(){
    controllerURL = "Controller/getCoConcepts.php";
    var newResultContainer = createResultContainer("Concept");
    controllerCall(getWikidataURLs(),controllerURL,newResultContainer,"Concept");
}

async function getThesisFromAdvisor(authorID) {
    controllerURL = "Controller/getThesisFromAdvisor.php";
    var newResultContainer = createResultContainer("Thesis");
    controllerCall(authorID,controllerURL,newResultContainer,"Thesis");
}

async function getThesisFromAuthor(authorID) {
    controllerURL = "Controller/getThesisFromAuthor.php";
    var newResultContainer = createResultContainer("Thesis");
    controllerCall(authorID,controllerURL,newResultContainer,"Thesis");
}

async function getThesisFromProgram(program) {
    controllerURL = "Controller/getThesisFromProgram.php";
    var newResultContainer = createResultContainer("Thesis");
    controllerCall(program,controllerURL,newResultContainer,"Thesis");
}

//  advisorBtn.setAttribute("onclick","getAdvisorFromAuthor('"+identifier+"')");
//conceptsBtn.setAttribute("onclick","getTopicsFromAuthor('"+identifier+"')");
async function getAdvisorFromAuthor(authorID) {
    controllerURL = "Controller/getAdvisorFromAuthor.php";
    var newResultContainer = createResultContainer("Advisor");
    controllerCall(authorID,controllerURL,newResultContainer,"Advisor");
}

async function getTopicsFromAuthor(authorID) {
    controllerURL = "Controller/getTopicsFromAuthor.php";
    var newResultContainer = createResultContainer("Concept");
    controllerCall(authorID,controllerURL,newResultContainer,"Concept");
}


async function getAuthorFromThesis(thesisID) {
    controllerURL = "Controller/getAuthorByThesis.php";
    var newResultContainer = createResultContainer("Author");
    controllerCall(thesisID,controllerURL,newResultContainer,"Author");
}

async function getAuthorFromAdvisor(authorID) {
    controllerURL = "Controller/getAuthorFromAdvisor.php";
    var newResultContainer = createResultContainer("Author");
    controllerCall(authorID,controllerURL,newResultContainer,"Author");
}

async function getAdvisorFromThesis(thesisID) {
    controllerURL = "Controller/getAdvisorByThesis.php";
    var newResultContainer = createResultContainer("Advisor");
    controllerCall(thesisID,controllerURL,newResultContainer,"Advisor");
}


async function getTopicsFromThesis(thesisID) {
    controllerURL = "Controller/getTopicsByThesis.php";
    var newResultContainer = createResultContainer("Concept");
    controllerCall(thesisID,controllerURL,newResultContainer,"Concept");
}

async function getTopicsFromAdvisor(advisorID) {
    controllerURL = "Controller/getTopicsFromAdvisor.php";
    var newResultContainer = createResultContainer("Concept");
    controllerCall(advisorID,controllerURL,newResultContainer,"Concept");
}

