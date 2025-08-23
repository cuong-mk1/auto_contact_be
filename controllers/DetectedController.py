from flask import Blueprint, request, jsonify, make_response
from producer.push_data_queue import create_queue_complete_form
from producer.push_data_name_queue import create_queue_find_company_url
from producer.read_csv_push_queue import read_csv_push_message_queue
from services.JobsService import JobService
from services.BlackListService import BlackListService
from services.OpenAIService import OpenAIService
from services.ExtractUrlService import find_url_from_company_name
from services.ExtractUrlService import process_response_gemini ,download_csv_by_id,find_url_from_company_name_v2
import os
selenium = Blueprint('selenium', __name__, url_prefix='/api')
API_KEY = os.getenv('API_KEY')

def check_api_key():
    api_key = request.headers.get('apikey')
    if api_key == API_KEY:
        return True
    return False

# @selenium.route('/submit-form', methods=['POST'])
# def handle_submit_form():
#     try:
#         data = request.json
#         print(f'data',data)
#         # url = data.get("url")
#         data_send = data["data_send"]
#         setting = data["setting"]
#         url = 'https://www.eeeemo.co.jp/otoiawase/'
#         result = submit_form(url, data_send,setting)
#         print(f'data',data)
#         return make_response(jsonify(result, 200))
#     except Exception as e:
#         return make_response(jsonify(str(e), 400))
# @selenium.route('/get_list_url_contact', methods=['POST'])
# def get_list_contact_url():
#     try:
#         data = request.json
#         print(f'data',data)
#         # url = data.get("url")
#         data_send = data["data_send"]
#         setting = data["setting"]
#         list_urls = data["list_urls"]
#         result = finding_contact_url(list_urls,data_send,setting)
#         print(f'data',data)
#         return make_response(jsonify(result, 200))
#     except Exception as e:
#         return make_response(jsonify(str(e), 400))
@selenium.route('/add_message_to_queue', methods=['POST'])
def add_message_to_queue():
    try:
        if check_api_key():
            data = request.json
            print(f'data',data)
            # url = data.get("url")
            result = create_queue_complete_form(data)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/get_histories', methods=['GET'])
def get_histories():
    try:
        # url = data.get("url")
        if check_api_key():
            print("Come here")
            limit = int(request.args.get('limit', 10))
            page = int(request.args.get('page', 1))
            result = JobService.get_list_job_histories(limit=limit,page=page)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/get_black_lists', methods=['GET'])
def get_black_lists():
    try:
        if check_api_key():
            result = BlackListService.get_black_list()
            data = {
                'urls': result
            }
            return make_response(jsonify(data, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/update_black_lists', methods=['POST'])
def update_black_lists():
    try:
        if check_api_key():
            data = request.json
            print(f'data',data)
            list_urls = data['urls']
            print(f'list_urls',list_urls)
            #convert to array
            result = BlackListService.update_black_list(list_urls)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/test_open_ai', methods=['GET'])
def test_open_ai():
    try:
        if check_api_key():
            # add url to params
            url = str(request.args.get('url'))
            result = OpenAIService.test_openai(url)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/find_company_url', methods=['POST'])
def find_company():
    try:
        if check_api_key():
            data = request.json
            print(f'data',data)
            company_name = data['company_name']
            print(f'company_name',company_name)
            #convert to array
            id = data['id']
            result = find_url_from_company_name(company_name,id)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/add_message_company_name_to_queue', methods=['POST'])
def add_message_company_to_queue():
    try:
        if check_api_key():
            data = request.json
            print(f'data',data)
            # url = data.get("url")
            result = create_queue_find_company_url(data)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@selenium.route('/get_company_histories', methods=['GET'])
def get_company_histories():
    try:
        # url = data.get("url")
        if check_api_key():
            print("Come here")
            limit = int(request.args.get('limit', 10))
            page = int(request.args.get('page', 1))
            result = JobService.get_list_upload_histories(limit=limit,page=page)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
# create api upload file csv
@selenium.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        if check_api_key():
            file_csv = request.files['file']
            print(f'file',file_csv)
            result = read_csv_push_message_queue(file_csv)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
# create api test search company name 
@selenium.route('/test_search_company_name', methods=['POST'])
def test_search_company_name():
    try:
        if check_api_key():
            data = request.json
            print(f'data',data)
            company_name = data['company_name']
            address = data['address']
            cooporation_number = data['cooporation_number']
            file_path_result = data['file_path_result']
            is_last_record = data['is_last_record']
            id = data['id']
            print(f'company_name',company_name)
            #convert to array
            result = find_url_from_company_name_v2(company_name,address,cooporation_number,file_path_result,is_last_record,id)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
#create api download file csv by id
@selenium.route('/download_csv_by_id', methods=['GET'])
def download_csv():
    try:
        if check_api_key():
            id = request.args.get('id')
            print(f'id',id)
            return download_csv_by_id(id)
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))