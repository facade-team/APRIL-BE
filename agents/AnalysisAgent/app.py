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

from flask import Flask, request

from agents.AnalysisAgent.pagent import Agent
from common import utils
from common.config import AnalysisAgentConfig as config
from common.config import InterfaceAgentConfig, RoutineManagementAgentConfig
from common.prompts.AnalysisAgentPrompt import pat_data

app = Flask(__name__)
agent = None


@app.route("/test", methods=["GET"])
def test():
    send_message("", config["name"])
    return "ok"


def send_message(message, send_to):
    envelope = {"message": message, "from": agent.name, "to": send_to}
    channel = utils.create_channel(send_to)
    channel.basic_publish(exchange="", routing_key=send_to, body=json.dumps(envelope))


def receive_messages():
    channel_name = agent.name
    channel = utils.create_channel(channel_name)

    # other agents
    routine_management_agent = RoutineManagementAgentConfig["name"]
    interface_agent = InterfaceAgentConfig["name"]

    def on_message_received(ch, method, properties, body):
        response = json.loads(body)
        print("received message : ", response)
        # TODO: Add business logic
        # Parse response (Who sent? In what format?)
        # Decide what to do next

        for pdata in pat_data:
            res = agent.chat(
                pdata["description"] + pdata["data"] + "2023-10-28" + " ??\n"
            )
            res_json = json.dumps(
                {
                    "type": pdata["type"],
                    "description": pdata["description"],
                    "estimated_time": res,
                }
            )
            print("Predict completed.\n" + res_json)
            send_message("Predict completed.\n" + res_json, routine_management_agent)

    channel.basic_consume(
        queue=channel_name, auto_ack=True, on_message_callback=on_message_received
    )

    channel.start_consuming()


if __name__ == "__main__":
    # Init Agent
    agent = Agent(config["name"], config["model"], None, config["sys_msg"])
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()
    app.run(debug=True, port=config["port"])
