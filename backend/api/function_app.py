# function_app.py (UPDATED to create item if not present)
import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.errors import CosmosResourceNotFoundError

app = func.FunctionApp()

# We can use a simple global variable to act as a cache once initialized (this helps to mock cosmos container for test)
cosmos_container = None

def get_cosmos_container():
    """Initializes and returns the Cosmos DB container client."""
    global cosmos_container
    if cosmos_container is not None:
        return cosmos_container

    # Read env variables here, when this function is called
    # Ensure these environment variables (COSMOS_ENDPOINT, COSMOS_KEY, etc.)
    # are set in your Azure Function App settings
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    db_name = os.environ["COSMOS_DATABASE"]
    container_name = os.environ["COSMOS_CONTAINER"]

    client = CosmosClient(endpoint, key)
    db = client.create_database_if_not_exists(id=db_name)
    # Important: The partition key path must match the field name in your documents (e.g., "/id")
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

    # Handle browser CORS preflight
    if req.method == "OPTIONS":
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
    item = None

    try:
        # 1. Try to read the existing item
        item = container.read_item(item=item_id, partition_key=item_id)
        # Item exists, increment count
        item["count"] += 1
        print(f"Item found and updated: ID {item_id}, new count {item['count']}")
    except CosmosResourceNotFoundError:
        # 2. Item does not exist, create it with initial values (id=1, count=0 initially + 1 for this visit)
        print(f"Item ID {item_id} not found. Creating a new one.")
        item = {"id": item_id, "count": 1}
    except Exception as e:
        # Handle other potential errors (e.g., connection issues)
        return func.HttpResponse(
            json.dumps({"error": f"An unexpected error occurred: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )

    # 3. Upsert (create or replace) the item in the database with the determined state
    try:
        # Use upsert_item to handle both the creation (after 404) and the update (if it was read successfully)
        container.upsert_item(body=item)
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Failed to save item to Cosmos DB: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )

    # Return the final count
    return func.HttpResponse(
        json.dumps({"visits": item["count"]}),
        mimetype="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )
