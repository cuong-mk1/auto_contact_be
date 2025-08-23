# Configure RabbitMQ connection
from config.rabbitmq import connect_rabbitmq
import pika
import json
from models.company_name_histories import CompanyNameHistories
from models.black_lists import BlackLists
from sqlalchemy import desc

def create_queue_find_company_url(payload):
    queue_name = "finding_company_url_queue"
    connection, channel = connect_rabbitmq(queue_name)
    list_company_names = payload.get('list_company_names')
    #insert to db
    dataInsert = CompanyNameHistories.bulk_create_data_company_name_histories(list_company_names)
    # Get json all object dataInsert
    dataInsert = [data.to_dict() for data in dataInsert]
    print(f'dataInsert',dataInsert)
    # push data insert to queue
    for objectUrl in dataInsert:
        message = json.dumps({
            'queue_name': queue_name,
            'signal': 'finding_company_url_queue',
            'company_name': objectUrl['company_name'],
            'id': objectUrl['id'],
        })
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
    print(f'Quantity account', len(list_company_names))
    connection.close()

    return {
        'message': f'create queue {queue_name} success',
        'total_urls': len(list_company_names)
    }
