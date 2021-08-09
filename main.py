from flask import Flask, render_template, request
import RPi.GPIO as GPIO
    
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)

lightOn = False

@app.route("/", methods=['GET', 'POST'])
def index():
    global lightOn
    print(request.method)

    if request.method == 'POST':
        if request.get_data() == b'lightSwitch':
            lightOn = (not lightOn)
            if lightOn:
                print("The light is now on")
                GPIO.output(23, GPIO.HIGH)
            else:
                print("The light is now off")
                GPIO.output(23, GPIO.LOW)
        else:
            return render_template("index.html", css="static/css/index.css", favicon="static/images/favicon.png", on="static/images/light-on.png", off="static/images/light-off.png", lightOn=lightOn)
    elif request.method == 'GET':
        print("No Post Back Call")
    return render_template("index.html", css="static/css/index.css", favicon="static/images/favicon.png", on="static/images/light-on.png", off="static/images/light-off.png", lightOn=lightOn)


if __name__ == '__main__':
    app.run(host="192.168.1.20", port=7070)
