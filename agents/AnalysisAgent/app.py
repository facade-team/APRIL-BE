import os
import sys

# 현재 파일의 절대 경로
current_file_path = os.path.abspath(__file__)
# 루트 디렉토리
root_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# sys.path에 루트 디렉토리 추가
sys.path.append(root_directory)

from flask import Flask, request
import threading
import json
from common import utils
from agents.agent import Agent
from common.config import InterfaceAgentConfig
from common.config import AnalysisAgentConfig as config
from common.config import RoutineManagementAgentConfig

app = Flask(__name__)
agent = None


def send_message(message, send_to):
    envelope = {
        "message": message,
        "from": agent.name,
        "to": send_to
    }
    channel = utils.create_channel(send_to)
    channel.basic_publish(exchange='',
                          routing_key=send_to,
                          body=json.dumps(envelope))


def receive_messages():
    channel_name = agent.name
    channel = utils.create_channel(channel_name)

    # other agents
    routine_management_agent = RoutineManagementAgentConfig["name"]
    interface_agent = InterfaceAgentConfig["name"]

    def on_message_received(ch, method, properties, body):
        response = json.loads(body)
        # TODO: Add business logic
        # Parse response (Who sent? In what format?)
        # Decide what to do next
        if response["from"] == routine_management_agent:  # send message to routine management agent
            my_msg = agent.chat(response["message"])
            send_message(my_msg, routine_management_agent)
        elif response["from"] == interface_agent:  # send message to interface agent
            my_msg = agent.chat(response["message"])
            send_message(my_msg, interface_agent)
        return

    channel.basic_consume(queue=channel_name,
                          auto_ack=True,
                          on_message_callback=on_message_received)

    channel.start_consuming()


if __name__ == '__main__':
    # Init Agent
    agent = Agent(config["name"], config["model"], None, config["sys_msg"])
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()
    app.run(debug=True, port=config["port"])
