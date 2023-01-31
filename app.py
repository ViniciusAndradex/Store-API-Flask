import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, "Bad request. Ensure 'name' is included in the JSON payload")
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message='Item already exists.')
    store_id = uuid.uuid4().hex # Valor temporário como id
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if ("price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data):
        abort(400, "Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload")
    if item_data["store_id"] not in stores:
        abort(404, mensage="Store not found")
    for item in items.values():
        if (item_data["name"] == items["name"] and item_data["store_id"] == items["store_id"]):
            abort(400, message='Item already exists.')
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return {"items": item}, 201
    


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return {"store": stores[store_id]}, 201
    except KeyError:
        abort(404, mensage="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return {"item": items[item_id]}, 201
    except KeyError:
        abort(404, mensage="Store not found")


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}
