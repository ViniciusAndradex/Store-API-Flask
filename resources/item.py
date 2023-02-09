import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchemas, ItemUpdateSchemas

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchemas)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class  ItemList(MethodView):
    @blp.response(200, ItemSchemas(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchemas)
    @blp.response(201, ItemSchemas)
    def post(self, item_data):
        for item in items.values():
            if (item_data["name"] == items["name"] and item_data["store_id"] == items["store_id"]):
                abort(400, message='Item already exists.')
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item