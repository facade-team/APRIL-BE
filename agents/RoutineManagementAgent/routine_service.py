import heapq
import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
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

    # routine_heap 을 출력
    print("===== routine heap =====")
    # if not routine_heap:
    #     print("No routine to execute")
    #     print()
    for execution_time, routine_id, routine_list in routine_heap:
        formatted_routine = {
            "routine_id": routine_id,
            "routine_list": routine_list,
            "execute_time": execution_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
        indented_output = json.dumps(formatted_routine, indent=4)
        print(indented_output)
        print()

    current_time = datetime.now()

    # Check if there are routines to execute
    while routine_heap and routine_heap[0][0] <= current_time:
        send_routine_to_MQ()


# routine 단 건을 message queue 에 보내는 함수
def send_routine_to_MQ():
    execution_time, routine_id, routine_list = heapq.heappop(routine_heap)

    execution_time = execution_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    dict_data = {
        "category": "routine",
        "body": {
            "routine_id": routine_id,
            "routine_list": routine_list,
            "execute_time": execution_time,
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
def add_routine_to_heap(execution_time, routine_id, routine_list):
    heapq.heappush(routine_heap, (execution_time, routine_id, routine_list))


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

    try:
        routine = Routine.query.get(routine_id)
        routine.routine_time = execute_time
        db.session.commit()

        # schedule 에 있는 루틴 정보도 수정하고 heap 을 재정렬
        for i in range(len(routine_heap)):
            if routine_heap[i][1] == routine_id:
                routine_heap[i] = (execute_time, routine_id, routine_heap[i][2])
                heapq.heapify(routine_heap)
                break

        return True
    except Exception as e:
        print(e)
        return False
