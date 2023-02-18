from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        raise NotImplementedError("Deleting a store is not implemented")

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)

        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id, **store_data)
        
        db.session.add(store)
        db.session.commit()

        return store

        
@blp.route("/store")
class StoresList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()


    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data): 
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")

        return store