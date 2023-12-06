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
    return response


@bp.route("/get-routine", methods=["GET"])
def get_routine():
    routine_list = routine_service.read_routines()

    routine_service.send_routine_list_to_MQ(routine_list)

    response = {"message": "Routine send successfully"}

    return response


# "ymd" = "20221222" 형식으로 넘어오는 쿼리파라미터
@bp.route("/get-routine-by-date", methods=["GET"])
def get_routine_by_date():
    ymd = request.args.get("ymd")

    routine_list = routine_service.read_routine_by_ymd(ymd)

    return routine_list


# 루틴의 서로 다른 ymd 리스트를 조회
@bp.route("/get-routine-ymd-list", methods=["GET"])
def get_routine_ymd_list():
    ymd_list = routine_service.read_routine_ymd_list()

    return ymd_list
