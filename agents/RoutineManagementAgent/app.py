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

from flask import Flask
from flask_migrate import Migrate

from agents.agent import Agent
from agents.RoutineManagementAgent import routine_controller, routine_service
from agents.RoutineManagementAgent.models import *
from common import utils
from common.config import AnalysisAgentConfig, InterfaceAgentConfig
from common.config import RoutineManagementAgentConfig as config
from common.database import DB_URL

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
agent = None


migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


def send_message(message, msg_from, send_to):
    envelope = {"message": message, "from": msg_from, "to": send_to}
    channel = utils.create_channel(send_to)
    channel.basic_publish(exchange="", routing_key=send_to, body=json.dumps(envelope))


def receive_messages():
    channel_name = agent.name
    channel = utils.create_channel(channel_name)

    # other agents
    analysis_agent = AnalysisAgentConfig["name"]
    interface_agent = InterfaceAgentConfig["name"]

    def on_message_received(ch, method, properties, body):
        response = json.loads(body)
        print("received message : ", response)

        # TODO: Add business logic
        # Parse response (Who sent? In what format?)
        # Decide what to do next

        # 1. 패턴분석 완료 => 루틴생성 + 스케쥴러 등록
        if response["from"] == analysis_agent:
            routine_list = agent.chat(response["message"])
            routine_service.save_routine(routine_list)

        elif response["from"] == interface_agent:  # send message to interface agent
            my_msg = agent.chat(response["message"])
            # send_message(my_msg, interface_agent)
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

    app.register_blueprint(routine_controller.bp)

    with app.app_context():
        db.create_all()

    routine_service.routine_scheduler.start()

    app.run(debug=True, port=config["port"])
