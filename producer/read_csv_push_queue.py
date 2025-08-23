# Configure RabbitMQ connection
from config.rabbitmq import connect_rabbitmq
import pika
import json
from models.upload_histories import UploadHistories
from sqlalchemy import desc
import csv
from datetime import datetime
import os
directory = 'file/'
if not os.path.exists(directory):
    os.makedirs(directory)
def read_csv_push_message_queue(csv_file):
    queue_name = "finding_company_url_queue"
    connection, channel = connect_rabbitmq(queue_name)
    #save file to folder upload
    csv_file.save(os.path.join(directory, csv_file.filename))
    file_path = os.path.join(directory, csv_file.filename)
    file_path_result = directory + 'result/' + datetime.now().strftime('%Y%m%d%H%M%S') + "_" + csv_file.filename
    # create data upload histories
    total_record = 0
    # check existed file name
    existed_file_name = UploadHistories.check_exist_file_name(csv_file.filename)
    if existed_file_name:
        return {
            'message': f'file name {csv_file.filename} is existed',
            'total_urls': 0
        }
    try:
        #open file csv
        with open('file/'+csv_file.filename, mode='r',encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # count record csv_reader
            total_record = sum(1 for row in csv_reader) - 1  # Subtract 1 for header row
            upload_histories = {
            'file_name': csv_file.filename,
            'file_path': file_path,
            'file_path_result': file_path_result,
            'status': 0,
            'created': datetime.now(),
            'number_of_records': total_record
            }
            data_created = UploadHistories.create_data_upload_histories(upload_histories)
            id_created = data_created.id
            file.seek(0)  # Reset file pointer to the beginning
            csv_reader = csv.reader(file)  # Reinitialize csv_reader
            next(csv_reader)  # Skip header row
            for index, row in enumerate(csv_reader):
                print('index',index)
                # check is last 
                is_last_record = False
                if (total_record - 1 == index):
                    is_last_record = True
                if len(row) >= 3:
                    company_name = row[1]
                    address = row[3]
                    cooporation_number = row[5]
                    file_name = csv_file.filename
                    message = json.dumps({
                        'queue_name': queue_name,
                        'signal': 'finding_company_url_queue',
                        'company_name': company_name,
                        'address': address,
                        'cooporation_number': cooporation_number,
                        'file_name': file_name,
                        'file_path': file_path,
                        'file_path_result': file_path_result,
                        'is_last_record': is_last_record,
                        'id': id_created
                    })
                    print(f'message',message)
                    channel.basic_publish(
                        exchange='',
                        routing_key=queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2  # Make message persistent
                        )
                    )
                    
                else:
                    print("[ng] Skipping row")
        connection.close()
        
    except Exception as e:
        print(f'Error',e)
    return {
        'message': 'success',
        'total_urls': total_record
    }
