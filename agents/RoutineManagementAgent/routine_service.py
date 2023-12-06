import heapq
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from agents.RoutineManagementAgent.app import send_message
from agents.RoutineManagementAgent.models import *

routine_heap = []
routine_scheduler = BackgroundScheduler()


def scheduled_job():
    print("scheduler : Checking routine...")

    # routine_heap 을 출력
    print("routine heap : ", routine_heap)

    current_time = datetime.now()

    # Check if there are routines to execute
    while routine_heap and routine_heap[0][0] <= current_time:
        send_routine_to_MQ()


# routine 을 message queue 에 보내는 함수
def send_routine_to_MQ():
    execution_time, routine_id, routineList = heapq.heappop(routine_heap)

    execution_time = execution_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    dict_data = {
        "category": "routine",
        "body": {
            "id": routine_id,
            "routineList": routineList,
            "execute_time": execution_time,
        },
    }

    json_data = json.dumps(dict_data)
    # print(json_data)
    send_message(json_data, "RoutineManagementAgent", "InterfaceAgent")  # mq 에 보내기


# Function to add routine to the heap
def add_routine_to_heap(execution_time, routine_id, routineList):
    heapq.heappush(routine_heap, (execution_time, routine_id, routineList))


def save_routine(message):
    for routine in message:
        execute_time = datetime.strptime(
            routine["execute_time"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        routine_instance = Routine(routine_time=execute_time)

        db.session.add(routine_instance)
        db.session.commit()

        # schedule 에 루틴 추가
        add_routine_to_heap(execute_time, routine_instance.id, routine["routineList"])

        for device_entry in routine["routineList"]:
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
