import datetime
import json

routine_id, rotineList, execution_time = (
    274,
    [
        {"device": "Blind", "power": "up", "level": 30},
        {"device": "TV", "power": "on", "level": None},
    ],
    datetime.datetime(2023, 12, 2, 6, 0, 0, 200),
)

execution_time = execution_time.strftime("%Y-%m-%dT%H:%M:%S.%f")


dict_data = {
    "category": "routine",
    "body": {
        "id": routine_id,
        "routineList": rotineList,
        "execute_time": execution_time,
    },
}


json_data = json.dumps(dict_data)
print(json_data)
