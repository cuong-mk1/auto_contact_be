# Configure RabbitMQ connection
from config.rabbitmq import connect_rabbitmq
import pika
import json
from models.job_histories import JobHistories
from models.black_lists import BlackLists
from sqlalchemy import desc
def get_black_list():
    black_list = BlackLists.query.all()
    black_list = [item.url for item in black_list]
    return black_list

def create_queue_complete_form(payload):
    queue_name = "auto_complete_form"
    connection, channel = connect_rabbitmq(queue_name)
    list_urls = payload.get('list_urls')
    data_send = payload.get('data_send')
    setting = payload.get('setting')
    setting_name = data_send.get('name_of_setting') if data_send.get('name_of_setting') is not None else None
    
    black_list = get_black_list()
    # remove domain existed in blacklist
    filtered_urls = []
    for url in list_urls:
        is_black_list = False
        for black in black_list:
            if black in url or url in black:
                is_black_list = True
                break
        if not is_black_list:
            filtered_urls.append(url)
    list_urls = filtered_urls
    #insert to db
    dataInsert = JobHistories.bulk_create_data_job_histories(list_urls,setting_name)
    # Get json all object dataInsert
    dataInsert = [data.to_dict() for data in dataInsert]
    print(f'dataInsert',dataInsert)
    # push data insert to queue
    for objectUrl in dataInsert:
        message = json.dumps({
            'queue_name': queue_name,
            'signal': 'complete_form',
            'url': objectUrl['url'],
            'id': objectUrl['id'],
            'data_send': data_send,
            'setting': setting
        })
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
    print(f'Quantity account', len(list_urls))
    connection.close()

    return {
        'message': f'create queue {queue_name} success',
        'total_urls': len(list_urls)
    }
