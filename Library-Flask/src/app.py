from flask import Flask
from flask_cors import CORS
import schedule
import threading

import router_fault_detection
import router_log_motor
import router_motor
import router_flow

from repository_fault_detection import FaultDetection
from repository_log_motor import LogMotor
from repository_motor import Motor

app = Flask(__name__)

CORS(
    app, 
    origins="*", 
    supports_credentials=True, 
    methods=['GET', 'OPTIONS']
)

router_fault_detection.router(app)
router_log_motor.router(app)
router_motor.router(app)
router_flow.router(app)

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

schedule.every(5).seconds.do(insert)

def schedule_loop():
    while True:
        schedule.run_pending()

t = threading.Thread(target=schedule_loop)
t.start()

if __name__ == '__main__':
    app.run(debug=True)