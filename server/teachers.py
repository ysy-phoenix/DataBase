from flask import Blueprint, jsonify, request
from utils import *
from db import *

teacher_blueprint = Blueprint("teacher", __name__)


@teacher_blueprint.route("/teachers", methods=["GET"])
def all_teachers():
    response = {"status": True}
    teachers = Teacher.query.all()
    response["teachers"] = [teacher.json() for teacher in teachers]
    return jsonify(response)
