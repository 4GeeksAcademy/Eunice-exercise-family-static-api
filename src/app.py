"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = jsonify(members)

    return response_body, 200


@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.get_json(silent=True)
    if request_body is None:
        return jsonify({"msg": "You must send information"}), 400
    if "first_name" not in request_body:
        return jsonify({"msg": "First name required"}), 400
    if "age" not in request_body:
        return jsonify({"msg": "Age required"}), 400
    if "lucky_numbers" not in request_body:
        return jsonify({"msg": "Lucky numbers required"}), 400
    id = jackson_family._generateId()
    if "id" in request_body:
        id = request_body["id"]

    member = {
        "id": id,
        "first_name": request_body["first_name"],
        "last_name": jackson_family.last_name,
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }

    jackson_family.add_member(member)
    return jsonify({"msg": "Completed"}), 200


@app.route("/member/<int:id>", methods=["GET"])
def get_a_member(id):
    member = jackson_family.get_member(id)

    if member is None:
        response_body = {
            "msg": "No member available"
        }
        return jsonify(response_body), 404
    return jsonify(member), 200


@app.route("/member/<int:id>", methods=["DELETE"])
def delete_a_member(id):
    member = jackson_family.get_member(id)

    if member is None:
        response_body = {
            "msg": "No member available"
        }
        return jsonify(response_body), 404

    jackson_family.delete_member(id)

    response_body = {
        "done": True
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
