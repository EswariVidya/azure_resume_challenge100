window.addEventListener('DOMContentLoaded', (e) => {
    getVisitorCount();
})

const functionAPIUrl = 'https://azrcfa-v0io0sh.azurewebsites.net/api/visits'
// const functionAPIUrl = 'https://azureresumecounter100.azurewebsites.net/api/visits'
const localFunctionAPI = 'http://localhost:7071/api/visits';

const getVisitorCount = () => {
    let count = 0;
    fetch(functionAPIUrl, {mode: 'cors'}).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called function API");
        count = response.visits;
        console.log(count);
        document.getElementById("jsViewCount").innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}