import heapq
import json
import threading
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from agents.RoutineManagementAgent.app import send_message
from agents.RoutineManagementAgent.models import *

routine_heap = []
routine_scheduler = BackgroundScheduler()


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return super().default(obj)


def scheduled_job():
    print("scheduler : Checking routine...")

    # thread id 출력
    print(threading.get_ident())

    # routine_heap 을 출력
    print("===== routine heap =====")
    # if not routine_heap:
    #     print("No routine to execute")
    #     print()
    for execute_time, routine_id, routine_list in routine_heap:
        # formatted_routine = {
        #     "routine_id": routine_id,
        #     "routine_list": routine_list,
        #     "execute_time": execute_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        # }
        # indented_output = json.dumps(formatted_routine, indent=4)
        # print(indented_output)
        print(f"routine_id : {routine_id}   execute_time : {execute_time}", end=" ")
        print()

    current_time = datetime.now()

    # Check if there are routines to execute
    while routine_heap and routine_heap[0][0] <= current_time:
        send_routine_to_MQ()


# app 이 실행될 때, DB 에서 루틴 정보를 읽어서 schedule 에 추가
# 현재 시간 기준으로 미래에 있는 루틴들만 schedule 에 추가
def init_routine_scheduler():
    # Fetch routines with associated devices using join
    # routines_with_devices = db.session.query(Routine).join(Device).all()

    # n+1 문제 해결
    routines_with_devices = (
        db.session.query(Routine).options(joinedload(Routine.devices)).all()
    )

    # Serialize using Marshmallow schema
    routine_schema = RoutineSchema(many=True)
    result = routine_schema.dump(routines_with_devices)

    for routine in result:
        execute_time = datetime.strptime(
            routine["execute_time"], "%Y-%m-%dT%H:%M:%S.%f"
        )

        # 현재 시간보다 미래에 있는 루틴만 schedule 에 추가
        if execute_time > datetime.now():
            # schedule 에 루틴 추가
            add_routine_to_heap(
                execute_time, routine["routine_id"], routine["routine_list"]
            )


# routine 단 건을 message queue 에 보내는 함수
def send_routine_to_MQ():
    execute_time, routine_id, routine_list = heapq.heappop(routine_heap)

    execute_time = execute_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    dict_data = {
        "category": "routine",
        "body": {
            "routine_id": routine_id,
            "routine_list": routine_list,
            "execute_time": execute_time,
        },
    }

    json_string = json.dumps(dict_data, indent=2)
    # print(json_data)
    send_message(json_string, "RoutineManagementAgent", "InterfaceAgent")  # mq 에 보내기


# 조회된 routine 리스트를 message queue 에 보내는 함수
def send_routine_list_to_MQ(routine_list):
    dict_data = {"category": "routine_list", "body": routine_list}

    # Use the custom encoder when converting to JSON
    json_string = json.dumps(dict_data, indent=2, cls=CustomEncoder)
    print(json_string)
    send_message(json_string, "RoutineManagementAgent", "InterfaceAgent")


# Function to add routine to the heap
def add_routine_to_heap(execute_time, routine_id, routine_list):
    heapq.heappush(routine_heap, (execute_time, routine_id, routine_list))


def save_routine(message):
    for routine in message:
        execute_time = datetime.strptime(
            routine["execute_time"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        routine_instance = Routine(routine_time=execute_time)

        db.session.add(routine_instance)
        db.session.commit()

        # schedule 에 루틴 추가
        add_routine_to_heap(execute_time, routine_instance.id, routine["routine_list"])

        for device_entry in routine["routine_list"]:
            device = Device(
                device=device_entry["device"],
                power=device_entry["power"],
                level=device_entry["level"],
            )
            routine_instance.devices.append(device)
            db.session.add(device)
            db.session.commit()


routine_scheduler.add_job(
    func=scheduled_job,
    trigger=IntervalTrigger(seconds=3),
    id="check_routine",
    name="Check Routine",
    replace_existing=True,
)


# Example usage in your service logic
def read_routines():
    # Fetch routines with associated devices using join
    # routines_with_devices = db.session.query(Routine).join(Device).all()

    # n+1 문제 해결
    routines_with_devices = (
        db.session.query(Routine).options(joinedload(Routine.devices)).all()
    )

    # Serialize using Marshmallow schema
    routine_schema = RoutineSchema(many=True)
    result = routine_schema.dump(routines_with_devices)

    return result


def update_routine_by_id(routine_id, execute_time):
    # routine_id 에 해당하는 routine 의 execute_time 을 update

    print(111111)

    try:
        routine = Routine.query.get(routine_id)

        # execute_time 을 datetime 객체로 변환
        execute_time = datetime.strptime(execute_time, "%Y-%m-%d %H:%M")

        routine.routine_time = execute_time
        db.session.commit()

        # schedule 에 있는 루틴 정보도 수정하고 heap 을 재정렬
        for i in range(len(routine_heap)):
            if routine_heap[i][1] == routine_id:
                print("*****routine_id, execute_time*****")
                print(routine_id, execute_time)
                routine_heap[i] = (execute_time, routine_id, routine_heap[i][2])
                heapq.heapify(routine_heap)
                break

        return True
    except Exception as e:
        print(e)
        return False


def read_routine_by_ymd(ymd):
    # Convert the provided ymd string to a datetime object
    date_obj = datetime.strptime(ymd, "%Y%m%d")

    # Construct the query

    routines_on_date = (
        db.session.query(Routine)
        .filter(
            func.extract("year", Routine.routine_time) == date_obj.year,
            func.extract("month", Routine.routine_time) == date_obj.month,
            func.extract("day", Routine.routine_time) == date_obj.day,
        )
        .order_by(Routine.routine_time.asc())
        .all()
    )

    # Serialize using Marshmallow schema
    routine_schema = RoutineSchema(many=True)
    result = routine_schema.dump(routines_on_date)

    return result


def read_routine_ymd_list():
    # Use func.date_format to format the routine_time column as %Y%m%d
    formatted_dates = (
        db.session.query(func.date_format(Routine.routine_time, "%Y%m%d"))
        .distinct()
        .order_by(Routine.routine_time.asc())
        .all()
    )

    # Extract the formatted dates from the result
    unique_dates = [date[0] for date in formatted_dates]

    return unique_dates
