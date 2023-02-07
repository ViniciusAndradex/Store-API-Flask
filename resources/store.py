import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return {"store": stores[store_id]}, 201
        except KeyError:
            abort(404, message="Store not found.")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

    def put(self, store_id):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(400, "Bad request. Ensure 'name' are included in the JSON payload")
        try:
            store = stores[store_id]
            store |= store_data

            return {"store": store}, 201
        except KeyError:
            abort(404, message="Store not found.")

@blp.route("/store")
class StoresList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(400, "Bad request. Ensure 'name' is included in the JSON payload")
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message='Store already exists.')
        store_id = uuid.uuid4().hex # Valor temporário como id
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
