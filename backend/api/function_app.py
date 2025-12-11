# function_app.py (UPDATED)
import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient, PartitionKey

app = func.FunctionApp()

# Move the client setup logic into a function or use singletons/lazy loading
# We can use a simple global variable to act as a cache once initialized (this helps to mock cosmos container for test)
cosmos_container = None

def get_cosmos_container():
    """Initializes and returns the Cosmos DB container client."""
    global cosmos_container
    if cosmos_container is not None:
        return cosmos_container

    # Read env variables here, when this function is called
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    db_name = os.environ["COSMOS_DATABASE"]
    container_name = os.environ["COSMOS_CONTAINER"]

    client = CosmosClient(endpoint, key)
    db = client.create_database_if_not_exists(id=db_name)
    cosmos_container = db.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id")
    )
    return cosmos_container

@app.function_name(name="visitorCounter")
@app.route(route="visits", auth_level=func.AuthLevel.ANONYMOUS)
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    # Get the initialized container instance *inside* the request handler
    container = get_cosmos_container()

    # Handle browser CORS preflight (rest of the logic remains the same)
    if req.method == "OPTIONS":
        # ... (CORS logic here) ...
        return func.HttpResponse(
            "",
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    # Normal GET logic - Update Counter
    item_id = "1"

    try:
        item = container.read_item(item=item_id, partition_key=item_id)
        item["count"] += 1
        container.upsert_item(item)
    except Exception:
        item = {"id": item_id, "count": 1}
        container.upsert_item(item)

    return func.HttpResponse(
        json.dumps({"visits": item["count"]}),
        mimetype="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )
