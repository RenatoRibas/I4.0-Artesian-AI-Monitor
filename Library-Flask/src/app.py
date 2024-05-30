from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from waitress import serve
import schedule
import threading

import router_auth
import router_fault_detection
import router_log_motor
import router_motor
import router_flow

from repository_fault_detection import FaultDetection
from repository_log_motor import LogMotor
from repository_motor import Motor

counter = 1

def insert():
    global counter

    fault_counter = 10

    Motor.insert()
    FaultDetection.insert(counter, fault_counter)
    LogMotor.insert(counter, fault_counter)

    if (counter == fault_counter):
        counter = 1
    else:
        counter += 1

schedule.every(300).seconds.do(insert)

def schedule_loop():
    while True:
        schedule.run_pending()

t = threading.Thread(target=schedule_loop)
t.start()

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'artesian-ai-monitor'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 43200

    jwt = JWTManager(app)

    CORS(
        app, 
        origins="*", 
        supports_credentials=True,
    )

    router_auth.router(app, jwt)
    router_fault_detection.router(app, jwt)
    router_log_motor.router(app, jwt)
    router_motor.router(app, jwt)
    router_flow.router(app, jwt)

    # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)