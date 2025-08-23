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
@analyze.route('/delete_job/<int:job_index>', methods=['DELETE'])
def delete_job(job_index):
    print(f"Received request to delete job with index: {job_index}")
    try:
        if check_api_key():
            result = AnalyzeService.delete_job_by_index(job_index)
            return make_response(jsonify(result, 200))
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
@analyze.route('/export_job_csv/<int:job_index>', methods=['GET'])
def export_csv(job_index):
    try:
        if check_api_key():
            csv_data, filename = AnalyzeService.export_csv_by_job_index(job_index)
            response = make_response(csv_data)
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            response.headers['Content-Type'] = 'text/csv'
            return response
        else:
            return make_response(jsonify("API key is invalid", 400))
    except Exception as e:
        return make_response(jsonify(str(e), 400))
