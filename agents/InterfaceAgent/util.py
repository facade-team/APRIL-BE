"""
IoT
"""
def parse_device_name(target):
    if target in ["light", "Light", "lamp", "Lamp"]: # light
        return "light"
    elif target in ["TV", "tv"]: # TV
        return "TV"
    elif target in ["blind", "Blind"]: # blind
        return "blind"
    elif target in ["AC", "ac", "Air conditioner", "Air Conditioner", "air conditioner"]: # AC
        return "AC"
    else:
        return ""


def routine_answer_template(routine_id, ex_time, operation_list):
    metadata = f"""
    [{routine_id}번 루틴]
    - 실행 시간 : {ex_time}
    - 실행 목록 :"""
    op_ans = ""
    for op in operation_list:
        dev_name = parse_device_name(op["device"])
        op_ans += f"\t{dev_name}: "
        if op["power"]:
            op_ans += f"전원 {op['power']} "
        if op["level"] and dev_name == "AC":
            op_ans += f"온도 {op['level']}°C "
        elif op["level"] and dev_name == "blind":
            op_ans += f"전개 {op['level']}% "
        op_ans += "\n"
    return metadata + "\n" + op_ans


def build_routine_list_answer(body):
    answer = ""
    for routine in body:
        routine_id = routine["id"] # 루틴 번호
        ex_time = routine["execute_time"] # 실행 시간
        operation_list = routine["routineList"] # 루틴을 구성하는 기기 조작 명령들
        answer += routine_answer_template(routine_id, ex_time, operation_list)
    return answer

