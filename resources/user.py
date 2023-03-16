from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import UserModel
from schemas import UsersSchema

blp = Blueprint("User", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UsersSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username aleready exists.")
        
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")
 
        return {"message": "User created sucessfully."}, 201
    

@blp.route("/register/<int:user_id>")
class User(MethodView):
    @blp.response(200, UsersSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")

        return {"message": "User deleted."}
    