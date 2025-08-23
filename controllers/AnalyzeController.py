from flask import Blueprint, request, jsonify, make_response
from services.AnalyzeService import AnalyzeService

import os
analyze = Blueprint('analyze', __name__, url_prefix='/api')
API_KEY = os.getenv('API_KEY')

def check_api_key():
    api_key = request.headers.get('apikey')
    if api_key == API_KEY:
        return True
    return False

@analyze.route('/get_list_job_group', methods=['GET'])
def get_list_job_group():
    try:
        if check_api_key():
            list_group_history = AnalyzeService.get_list_group_history()
            return make_response(jsonify(list_group_history, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
