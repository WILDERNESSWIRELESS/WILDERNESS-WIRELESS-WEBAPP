from flask import Flask, render_template, redirect, jsonify, request
from time import sleep
from forms import BatLoForm, BatHiForm, CmdForm
import time
import smbus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(19, GPIO.OUT)

bus = smbus.SMBus(1)

avraddr = 0x77

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aassddff'

@app.route('/_get_time')

def get_time():
    transmit('{"cmd":"time"}')
    sleep(0.1)
    return jsonify(time=receive(10))

@app.route('/', methods=['GET','POST'])

def index():

    batloform = BatLoForm()
    bathiform = BatHiForm()
    cmdform   = CmdForm()

    if batloform.validate_on_submit():
        print(batloform.batloval.data)
        cmd1 = '{"batlo":"'+str(batloform.batloval.data)+'"}'
        transmit(cmd1)
        return redirect('/')

    if bathiform.validate_on_submit():
        print(bathiform.bathival.data)
        cmd2 = '{"bathi":"'+str(bathiform.bathival.data)+'"}'
        transmit(cmd2)
        return redirect('/')

    if cmdform.validate_on_submit():
        cmd = str(cmdform.cmdval.data)
        print cmd
        cmd3 = '{"cmd":"'+cmd+'"}'
        transmit(cmd3)
        sleep(0.1)
        if(cmd  == "time"):
            print(receive(10))
        return redirect('/')
    return render_template('index.html', title='form', batloform=batloform, bathiform=bathiform, cmdform=cmdform)

def transmit(msg):
    waitForBus(3)
    for char in msg:
        bus.write_byte(avraddr, ord(char))
        sleep(0.01)
    GPIO.output(19, GPIO.LOW)

def receive(numBytes):
    receivedBytes = None
    receivedMessage = None
    waitForBus(3)
    try:
        receivedBytes = bus.read_i2c_block_data(avraddr, 0x00, numBytes)
    except:
        print("Error.")
    receivedMessage= str(bytearray(receivedBytes))
    GPIO.output(19, GPIO.LOW)
    return receivedMessage

def waitForBus(t):
    print("Waiting for control of i2c bus")
    timeout = time.time()+t
    while GPIO.input(26):
        if time.time() > timeout:
            break;
    GPIO.output(19, GPIO.HIGH)
    sleep(0.1)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

