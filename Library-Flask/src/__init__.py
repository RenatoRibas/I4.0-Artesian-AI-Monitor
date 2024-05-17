from flask import Flask
from flask_cors import CORS
import schedule
import threading

import router_previsao
import router_log_motor
import router_motor
import router_vazao

from repositorio_previsao import Previsao
from repositorio_log_motor import LogMotor
from repositorio_motor import Motor

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True, methods=['GET', 'OPTIONS'])

router_previsao.router(app)
router_log_motor.router(app)
router_motor.router(app)
router_vazao.router(app)

counter = 1

def insert():
    global counter

    Motor.insert()
    Previsao.insert(counter)
    LogMotor.insert(counter)

    if (counter == 10):
        counter = 0
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