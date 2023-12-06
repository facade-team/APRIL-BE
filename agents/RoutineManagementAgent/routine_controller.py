from datetime import datetime

from flask import Blueprint, jsonify, request

from agents.RoutineManagementAgent import routine_service
from agents.RoutineManagementAgent.models import *

bp = Blueprint("main", __name__, url_prefix="/")


# POST 요청으로 body 에 패턴 정보를 담아서 보냄
@bp.route("/create-routine", methods=["POST"])
def create_routine():
    # Get the JSON data from the request body
    data = request.get_json()
    data = data["data"]

    # print(data)

    # Access the data, perform operations, and return a response
    routine_service.save_routine(data)

    # Return a response
    response = {"message": "Routine created successfully"}
    return jsonify(response)


@bp.route("/get-routine", methods=["GET"])
def get_routine():
    routine_list = routine_service.read_routines()

    return routine_list
