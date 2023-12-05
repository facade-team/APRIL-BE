import os
import sys

# 현재 파일의 절대 경로
current_file_path = os.path.abspath(__file__)
# 루트 디렉토리
root_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# sys.path에 루트 디렉토리 추가
sys.path.append(root_directory)

import json
import threading
from datetime import datetime, timedelta

import requests
from chat import build_chat, parse_agent_answer
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from agents.agent import Agent
from common import utils
from common.config import SMART_HOME_API_BASE, AnalysisAgentConfig
from common.config import InterfaceAgentConfig as config
from common.config import RoutineManagementAgentConfig

app = Flask(__name__)
socketio = SocketIO(app)
agent = None
delimiter = config["delimiter"]

# other agents
analysis_agent = AnalysisAgentConfig["name"]
routine_management_agent = RoutineManagementAgentConfig["name"]

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

"""
Communicate with User via SocketIO
"""


@app.route("/")
def index():
    return render_template("index.html")  # temp page for socketIO test


@socketio.on("chat")
def handle_chat_message(message):
    emit("chat", build_chat("user", message), broadcast=True)  # broadcast user message
    agent_answer = agent.chat(
        f"{delimiter}{message}{delimiter}"
    )  # ask to interface agent
    parsed_answer = json.loads(agent_answer)
    category, requirements, answer = (
        parsed_answer["category"],
        parsed_answer["requirements"],
        parsed_answer["answer"],
    )
    print(parsed_answer)
    if category == "Execute IoT Routine":
        routine_number = requirements["routine_number"]
        when_to_execute_in_hours = requirements["when_to_execute_in_hours"]
        ex_time = datetime.now() + timedelta(hours=when_to_execute_in_hours)
        ex_time = ex_time.strftime("%Y-%m-%d %H:%M")
        # Routine-Management Agent에 modify 요청
        send_message(
            {"category": "modify", "body": {"id": routine_number, "time": ex_time}},
            routine_management_agent,
        )
    elif category == "Modify IoT Routine":
        routine_number = requirements["routine_number"]
        new_time = requirements["time"]
        new_hour, new_minute = map(int, new_time.split(":"))
        ex_time = datetime.now().replace(hour=new_hour, minute=new_minute)
        ex_time = ex_time.strftime("%Y-%m-%d %H:%M")
        # Routine-Management Agent에 modify 요청
        send_message(
            {"category": "modify", "body": {"id": routine_number, "time": ex_time}},
            routine_management_agent,
        )
    elif category == "Operate IoT Devices":
        device = parse_device_name(requirements["device"])
        if device == "":
            print("Error! Unsupported Device") # TODO : 예외 처리
        operation = requirements["operation"]
        data = {"type": device, "operation": operation}
        headers = {"Content-Type": "application/json"}
        r = requests.post(
            SMART_HOME_API_BASE + "/device", data=json.dumps(data), headers=headers
        )
        print(r.text)
    elif category == "Search IoT Routine":
        # Routine-Management Agent에게 search 요청
        send_message({"category": "search", "body": {}}, routine_management_agent)
    elif category == "General Query":
        pass
    else:
        print("Error: Invalid Answer")
        emit(
            "chat", build_chat("agent", "오류가 발생했습니다."), broadcast=True, namespace="/"
        )  # broadcast agent message
        return
    emit(
        "chat", build_chat("agent", answer), broadcast=True, namespace="/"
    )  # broadcast agent message
    return


"""
Communicate with Agents via Message Broker Server
"""


def send_message(message, send_to):
    envelope = {"message": message, "from": agent.name, "to": send_to}
    channel = utils.create_channel(send_to)
    channel.basic_publish(exchange="", routing_key=send_to, body=json.dumps(envelope))


def receive_messages():
    channel_name = agent.name
    channel = utils.create_channel(channel_name)

    def on_message_received(ch, method, properties, body):
        response = json.loads(body)
        if response["from"] == analysis_agent:  # send message to analysis agent
            # my_msg = agent.chat(response["message"])
            # send_message(my_msg, analysis_agent)
            pass
        elif (
            response["from"] == routine_management_agent
        ):  # send message to routine managent agent
            message = response["message"]
            if message["category"] == "routine":
                # 루틴 실행
                routine_list = message["body"]["routineList"]
                headers = {"Content-Type": "application/json"}
                body = []
                for op in routine_list:
                    dev_name = parse_device_name(parse_device_nameop["device"])
                    if dev_name == "":
                        print("Error! Unsupported Device") # TODO : 예외 처리
                    body.append({
                        "type": dev_name,
                        "operation": {
                            "power": op["power"],
                            "level": op["level"]
                        }
                    })
                r = requests.post(
                    SMART_HOME_API_BASE + "/devices", data=json.dumps(data), headers=headers
                )
                print(r.text)
            else:
                # 결과 유저에게 전달
                pass
        return

    channel.basic_consume(
        queue=channel_name, auto_ack=True, on_message_callback=on_message_received
    )

    channel.start_consuming()


if __name__ == "__main__":
    # Init Agent
    agent = Agent(config["name"], config["model"], None, config["sys_msg"])
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()
    socketio.run(app, debug=True, port=config["port"])
