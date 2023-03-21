from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import jwt_redis_blocklist, ACCESS_EXPIRE
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
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UsersSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
 
        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefrsh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.append("jti", jti)
        return {"access_token": new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, ex=ACCESS_EXPIRE)
        return {"message": "Successfully logged out."}


@blp.route("/register/<int:user_id>")
class User(MethodView):
    @blp.response(200, UsersSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")

        return {"message": "User deleted."}
    