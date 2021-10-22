from flask import Flask, render_template, request
from flask import jsonify
import RPi.GPIO as GPIO
import schedule
import time
from multiprocessing import Process, Value

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)

lightOn = False

def switchLight ():
    global lightOn
    lightOn = (not lightOn)
    if lightOn:
        print("The light is now on")
        GPIO.output(23, GPIO.HIGH)
    else:
        print("The light is now off")
        GPIO.output(23, GPIO.LOW)

def turnLightOn ():
    global lightOn
    lightOn = True
    print("The light has been turned on by a scheduled job.")
    switchLight()

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.get_data() == b'lightSwitch':
            switchLight()
    return render_template("index.html", css="static/css/index.css", favicon="static/images/favicon.png", on="static/images/light-on.png", off="static/images/light-off.png", lightOn=lightOn)

@app.route('/_stuff', methods=['GET'])
def stuff():
    return jsonify(lightOn=lightOn)  

def scheduleJobsAndLoop ():
    schedule.every().day.at("07:30").do(turnLightOn)

    print("")
    print(schedule.get_jobs())
    print("")

    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()

if __name__ == '__main__':
    p = Process(target=scheduleJobsAndLoop)
    p.start()
    app.run(host="192.168.1.20")
    p.join()
