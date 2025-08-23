from flask import Blueprint, request, jsonify, make_response
from services.SettingService import SettingService

import os
setting = Blueprint('setting', __name__, url_prefix='/api')
API_KEY = os.getenv('API_KEY')

def check_api_key():
    api_key = request.headers.get('apikey')
    if api_key == API_KEY:
        return True
    return False

@setting.route('/save-setting', methods=['POST'])
def save_data_setting():
    data = request.json
    print(f'data',data)
    try:
        if check_api_key():
            list_group_history = SettingService.save_setting_data(data)
            return make_response(jsonify(list_group_history, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@setting.route('/get-setting', methods=['GET'])
def get_setting():
    try:
        if check_api_key():
            setting_data = SettingService.get_setting_data()
            return make_response(jsonify(setting_data, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@setting.route('/get-list-setting', methods=['GET'])
def get_list_setting():
    try:
        if check_api_key():
            setting_data = SettingService.get_all_setting_data()
            return make_response(jsonify(setting_data, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
#get by id
@setting.route('/get-setting-by-id', methods=['GET'])
def get_setting_by_id():
    try:
        if check_api_key():
            id = request.args.get('id')
            setting_data = SettingService.get_setting_data_by_id(id)
            return make_response(jsonify(setting_data, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
