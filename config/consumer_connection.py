import pika
import os
from dotenv import load_dotenv
import ssl
load_dotenv()
HOSTNAME_MQ = os.getenv('HOSTNAME_MQ')
USERNAME_MQ = os.getenv('USERNAME_MQ')
PASSWORD_MQ = os.getenv('PASSWORD_MQ')
PORT_MQ = os.getenv('PORT_MQ')
VIRTUAL_HOST_MQ = os.getenv('VIRTUAL_HOST_MQ')

def connection_rabbitmq():
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
    # url = f"amqps://{USERNAME_MQ}:{PASSWORD_MQ}@{HOSTNAME_MQ}:5672"
    # print(url)
    credentials = pika.PlainCredentials(username=USERNAME_MQ, password=PASSWORD_MQ, erase_on_connect=True)
    parameters = pika.ConnectionParameters(host=HOSTNAME_MQ, port=PORT_MQ, virtual_host="/", credentials=credentials,heartbeat=600,blocked_connection_timeout=300)
    # parameters = pika.URLParameters(url)
    # parameters.ssl_options = pika.SSLOptions(context=ssl_context)
    connection = pika.BlockingConnection(parameters)
    return connection
