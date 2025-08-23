from flask import Flask, request, jsonify, make_response, g
from controllers.DetectedController import selenium
from controllers.AnalyzeController import analyze
from controllers.SettingController import setting

import threading
# import worker 
import worker.process_complete_form as process_complete_form
import worker.process_find_company_url as process_find_company_url
from flask_cors import CORS

from models.databaseConfig import db
from pymongo import MongoClient
from flask_apscheduler import APScheduler
import pytz
import os
from dotenv import load_dotenv
load_dotenv()
import json
# Job configuration class
class Config:
    SCHEDULER_API_ENABLED = True  # Enables the Flask-APScheduler API
# Set the timezone
timezone = pytz.timezone('UTC')
app = Flask(__name__)
# Flask app configuration
cors = CORS(app, resources={r"/*": {"origins": "*"}})
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# Get the values
DB_URI = os.getenv('DB_URI')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_APPNAME = os.getenv('DB_APPNAME')
DB_PORT = os.getenv('DB_PORT')

# Configure the SQLAlchemy part of the app instance
# Get config settings from .env file
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the SQLAlchemy db instance with the app

app.register_blueprint(selenium)
app.register_blueprint(analyze)
app.register_blueprint(setting)


db.init_app(app)
def run_worker():
    with app.app_context():
        process_complete_form.start_worker()
def run_find_company_url():
    with app.app_context():
        process_find_company_url.start_worker()

def start_threads(thread_functions, num_threads):
    threads = []
    for _ in range(num_threads):
        for thread_function in thread_functions:
            thread = threading.Thread(target=thread_function)
            threads.append(thread)
    for thread in threads:
        thread.start()
    return threads
# Start threads for workers
worker_threads = start_threads([run_worker], 1)
# company_name_threads = start_threads([run_find_company_url], 3)
if __name__ == "__main__":
    # Start RabbitMQ consumer in a separate thread for local runs
    # thread = threading.Thread(target=run_worker)
    # thread.start()
    app.run(debug=True,threaded=True,port=5004)