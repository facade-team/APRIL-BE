import pika
from enum import Enum

def create_channel(queue_name):
    # RabbitMQ에 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 메시지 큐 선언
    channel.queue_declare(queue=queue_name)

    return channel


class LogType(Enum):
    """
    [log type]
    - MQ 메세지 consume
    - MQ 메세지 publish
    - socketIO 메시지 read
    - socketIO 메시지 emit
    - agent에게 request
    - agent에게 response
    """
    MQ_CONSUME = "Message Consume"
    MQ_PUBLISH = "Message Publish"
    SOCKET_READ = "SocketIO Read"
    SOCKET_EMIT = "SocketIO Emit"
    AGENT_REQ = "Request to Agent"
    AGENT_RES = "Response from Agent"
def logger(log_type, msg):
    log = f"[{log_type.value}] {msg}"
    print(log)
    return