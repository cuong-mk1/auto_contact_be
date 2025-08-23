# Configure RabbitMQ connection
import os
from dotenv import load_dotenv

load_dotenv()

HOSTNAME_MQ = os.getenv('HOSTNAME_MQ')
USERNAME_MQ = os.getenv('USERNAME_MQ')
PASSWORD_MQ = os.getenv('PASSWORD_MQ')
PORT_MQ = os.getenv('PORT_MQ')
VIRTUAL_HOST_MQ = os.getenv('VIRTUAL_HOST_MQ')
import pika
import ssl
def connect_rabbitmq(queue_name):
    # url = f"amqp://{USERNAME_MQ}:{PASSWORD_MQ}@{HOSTNAME_MQ}:5672"
    credentials = pika.PlainCredentials(username=USERNAME_MQ, password=PASSWORD_MQ, erase_on_connect=True)
    parameters = pika.ConnectionParameters(host=HOSTNAME_MQ, port=PORT_MQ, virtual_host="/", credentials=credentials,heartbeat=60)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # Declare a queue with the job name
    channel.queue_declare(queue=queue_name, durable=True)  # Durable to persist tasks
    return connection, channel