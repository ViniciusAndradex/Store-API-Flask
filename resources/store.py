import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchemas

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchemas)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreSchemas)
    @blp.response(200, StoreSchemas)
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(404, message="Store not found.")

@blp.route("/store")
class StoresList(MethodView):
    @blp.response(200, StoreSchemas(many=True))
    def get(self):
        return stores.values()


    @blp.arguments(StoreSchemas)
    @blp.response(201, StoreSchemas)
    def post(self, store_data): 
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message='Store already exists.')
        store_id = uuid.uuid4().hex # Valor temporário como id
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
#Corrigir o Buscar loja por id.