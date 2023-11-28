import pika

def create_channel(queue_name):
    # RabbitMQ에 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 메시지 큐 선언
    channel.queue_declare(queue=queue_name)

    return channel