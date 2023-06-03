from flask import Blueprint, jsonify, request
from utils import *
from db import *

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login/register", methods=["PUT"])
def register():
    response_object = {"status": "success"}
    post_data = request.get_json()
    response_object["flag"] = False

    user = User.query.filter_by(username=post_data.get("username")).first()
    if user is not None:  # case1
        response_object["message"] = "Account already exists!"
        return jsonify(response_object)

    teacher = Teacher.query.filter_by(No=post_data.get("username")).first()
    if teacher is None:  # case2
        response_object["message"] = "No such teacher!"
    else:  # case3
        add_user(post_data.get("username"), post_data.get("password"))
        response_object["message"] = "Create account successfully!"
        response_object["flag"] = True
    return jsonify(response_object)


@login_blueprint.route("/login/login", methods=["PUT"])
def login():
    response_object = {"status": "success"}
    response_object["flag"] = False
    post_data = request.get_json()
    user = User.query.filter_by(username=post_data.get("username")).first()
    if user is None:  # case1
        response_object["message"] = "No such teacher!"
    elif user.password != post_data.get("password"):  # case2
        response_object["message"] = "Password incorrect!"
    else:  # case3
        response_object["message"] = "Success!"
        response_object["flag"] = True
    return jsonify(response_object)
