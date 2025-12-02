window.addEventListener('DOMContentLoaded', (event) => {
        getVisitorCount();
})

const functionAPI = 'http://localhost:7071/api/visits';

const getVisitorCount = () => {
    let count = 0;
    fetch(functionAPI, {mode: 'cors'}).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called function API");
        count = response.visits;
        document.getElementById("jsViewCount").innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}