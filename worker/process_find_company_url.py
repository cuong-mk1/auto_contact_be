import pika
import time
import json
from producer.common import list_queue_name
import os
from dotenv import load_dotenv
load_dotenv()
from services.ExtractUrlService import process_response_gemini
from services.ExtractUrlService import find_url_from_company_name_v2
HOSTNAME_MQ = os.getenv('HOSTNAME_MQ')
import config.consumer_connection as consumer_connection
def callback(ch, method, properties, body):
    print(f"body: {body}")
    try:
        data = json.loads(body)
        print(f"Đang xử lý task: {data}")
        # Xác nhận thông báo khi xử lý thành công
        company_name = data.get('company_name')
        address = data.get('address')
        cooporation_number = data.get('cooporation_number')
        file_path_result = data.get('file_path_result')
        is_last_record = data.get('is_last_record')
        id = data.get('id')
        # process_response_gemini(company_name,address,cooporation_number,file_path_result,is_last_record,id)
        response = find_url_from_company_name_v2(company_name,address,cooporation_number,file_path_result,is_last_record,id)
        if response == 'LIMIT_SEARCH_BY_DAY':
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print("Task đưa vào lại hàng đợi do vượt quá số lần tìm kiếm trong ngày")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Task được xử lý thành công")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        # Nếu xảy ra lỗi, đưa vào lại hàng đợi
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        # ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Task đưa vào lại hàng đợi")
def start_worker():
    queue_name = "finding_company_url_queue"
    # Connect to RabbitMQ
    connection = consumer_connection.connection_rabbitmq()
    # connection = pika.BlockingConnection(pika.ConnectionParameters(HOSTNAME_MQ))
    channel = connection.channel()
    # Ensure the queue exists
    channel.queue_declare(queue=queue_name, durable=True)
    # Tell RabbitMQ that this worker can handle one task at a time
    channel.basic_qos(prefetch_count=1)
    # Start consuming tasks from the 'task_queue'
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Worker started. Waiting for tasks...")
    channel.start_consuming()

# if __name__ == "__main__":
#     start_worker()