from agents.agent import Agent
from agents.RoutineManagementAgent import app
from agents.RoutineManagementAgent.models import *


def save_routine(message):
    for routine in message:
        execute_time = datetime.strptime(
            routine["execute_time"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        routine_instance = Routine(routine_time=execute_time)
        db.session.add(routine_instance)

        for device_entry in routine["routineList"]:
            device = Device(
                device=device_entry["device"],
                power=device_entry["power"],
                level=device_entry["level"],
            )
            routine_instance.devices.append(device)
            db.session.add(device)

    db.session.commit()
