from datetime import datetime

from flask import Blueprint, jsonify, request

from agents.RoutineManagementAgent.models import *
from agents.RoutineManagementAgent.routine_service import *

bp = Blueprint("main", __name__, url_prefix="/")

# POST 요청으로 body 에 패턴 정보를 담아서 보냄


@bp.route("/create-routine", methods=["POST"])
def create_routine():
    # Get the JSON data from the request body
    data = request.get_json()
    data = data["data"]

    print(data)

    # Access the data, perform operations, and return a response

    save_routine(data)

    # Return a response
    response = {"message": "Routine created successfully"}
    return jsonify(response)
