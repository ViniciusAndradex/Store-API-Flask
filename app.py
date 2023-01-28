from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My store",
        "items": [
            {
                "name": "table",
                "price": 19.99
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    for store in stores:
        if store["name"] == request_data["name"]:
            return {"mensage": "There is already a store with that name"}, 400
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return {"items": store["items"]}, 201
    return {"mensage": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return {"store": store}, 201
    return {"mensage": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}, 201
    return {"mensage": "Store not found"}, 404