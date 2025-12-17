(() => {
  // ====== CONFIG ======
  // Highest priority: runtime-configured API base (stamped by CI)
  const API_BASE =
    (window.__APP_CONFIG__ && typeof window.__APP_CONFIG__.apiBase === 'string'
      ? window.__APP_CONFIG__.apiBase
      : ''
    ).replace(/\/+$/, ''); // trim trailing /

  // Define hardcoded fallback URL here to be referenced later
//   const FALLBACK_API_URL = 'https://azrcfa-v0io0sh.azurewebsites.net/api/visits';

  window.addEventListener('DOMContentLoaded', (e) => {
      getVisitorCount();
  });

  // Recoded this line to use API_BASE if set, otherwise use the fallback URL.
  const ENDPOINT = API_BASE ? `${API_BASE}/api/visits` : null;
  

  // The original hardcoded variables are now redundant but kept for context:
  // const functionAPIUrl = 'https://azrcfa-v0io0sh.azurewebsites.net/api/visits'
  // const localFunctionAPI = 'http://localhost:7071/api/visits';

  const getVisitorCount = () => {
      // Add a check to prevent fetch errors if ENDPOINT somehow ends up null/undefined
      if (!ENDPOINT) {
          console.error("API ENDPOINT is not configured.");
          document.getElementById("jsViewCount").innerText = "Error";
          return;
      }

      console.log(`Fetching from: ${ENDPOINT}`);
      
      let count = 0;
      fetch(ENDPOINT, {mode: 'cors'}).then(response => {
          if (!response.ok) { // Basic error check for HTTP status codes
              throw new Error(`Network response was not ok: ${response.statusText}`);
          }
          return response.json();
      }).then(response => {
          console.log("Website called function API");
          count = response.visits;
          console.log(count);
          document.getElementById("jsViewCount").innerText = count;
      }).catch(function(error){
          console.error("Fetch error:", error);
          document.getElementById("jsViewCount").innerText = "Failed";
      });
      // Note: The returned 'count' here is 0 because the fetch is asynchronous. 
      // The DOM update happens inside the second .then() block.
      // return count; 
  }

})();