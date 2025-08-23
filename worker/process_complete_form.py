import pika
import time
import json
from producer.common import list_queue_name
import os
from dotenv import load_dotenv
from models.job_histories import JobHistories
load_dotenv()
# from services.ContactService import submit_form
from services.BrowserUseService import submit_form
import asyncio
HOSTNAME_MQ = os.getenv('HOSTNAME_MQ')
import config.consumer_connection as consumer_connection
async def async_callback(ch, method, properties, body):
    print(f"body: {body}")
    try:
        data = json.loads(body)
        print(f"Đang xử lý task: {data}")
        # Xác nhận thông báo khi xử lý thành công
        url = data.get('url')
        data_send = data.get('data_send')
        setting = data.get('setting')
        id = data.get('id')
        # check if id exists in database
        job_history = JobHistories.query.get(id)
        if not job_history:
            print(f"Job history with id {id} not found")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        try:
            await submit_form(url, data_send, setting, id)
        except Exception as e:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            JobHistories.update_status(id, 3, str(e))
        print("Task được xử lý thành công")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        # update status to 3
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if job_history:
            JobHistories.update_status(id, 3, str(e))
def sync_callback(ch, method, properties, body):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If the event loop is already running, create a task
        asyncio.create_task(async_callback(ch, method, properties, body))
    else:
        # If no event loop is running, run the async function
        loop.run_until_complete(async_callback(ch, method, properties, body))
def start_worker():
    queue_name = "auto_complete_form"
    while True:
        try:
            # Create and set an event loop for the current thread
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            # Connect to RabbitMQ
            connection = consumer_connection.connection_rabbitmq()
            channel = connection.channel()
            # Ensure the queue exists
            channel.queue_declare(queue=queue_name, durable=True)
            # Tell RabbitMQ that this worker can handle one task at a time
            channel.basic_qos(prefetch_count=1)
            # Start consuming tasks from the 'task_queue'
            channel.basic_consume(queue=queue_name, on_message_callback=sync_callback)
            print("Worker started. Waiting for tasks...")
            channel.start_consuming()
        except Exception as e:
            print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before reconnecting

# if __name__ == "__main__":
#     start_worker()