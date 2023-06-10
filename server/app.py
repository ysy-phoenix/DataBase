import uuid
from urllib.parse import quote_plus
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils import *
from db import *
from login import *
from paper import *
from project import *
from course import *
from query import *
from teachers import *

# create the app
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:%s@localhost:3306/lab3" % quote_plus("13058873998ysy@")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.register_blueprint(login_blueprint)
app.register_blueprint(paper_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(course_blueprint)
app.register_blueprint(query_blueprint)
app.register_blueprint(teacher_blueprint)
db.init_app(app)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# sanity check route
@app.route("/", methods=["GET"])
def ping_pong():
    return jsonify("Hello!")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        init_data()
    app.run()
