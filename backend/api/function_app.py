import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient, PartitionKey

app = func.FunctionApp()

# Cosmos env variables
endpoint = os.environ["COSMOS_ENDPOINT"]
key = os.environ["COSMOS_KEY"]
db_name = os.environ["COSMOS_DATABASE"]
container_name = os.environ["COSMOS_CONTAINER"]

client = CosmosClient(endpoint, key)
db = client.create_database_if_not_exists(id=db_name)
container = db.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

@app.function_name(name="visitorCounter")
@app.route(route="visits", auth_level=func.AuthLevel.ANONYMOUS)
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:

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
        mimetype="application/json"
    )