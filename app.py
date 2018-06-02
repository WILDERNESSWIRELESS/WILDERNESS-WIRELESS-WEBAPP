from flask import Flask, render_template, redirect
from flask import request
from time import sleep
from forms import BatLoForm, BatHiForm, CmdForm
import time
import smbus
#from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(19, GPIO.OUT)

bus = smbus.SMBus(1)
#bus = SMBus(1)

eepromaddr = 0x50

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aassddff'

@app.route('/', methods=['GET','POST'])
def index():
    batloform = BatLoForm()
    bathiform = BatHiForm()
    cmdform   = CmdForm()
    if batloform.validate_on_submit():
        print(batloform.batloval.data)
        cmd1 = '{"batlo":"'+str(batloform.batloval.data)+'"}'
        while GPIO.input(26):
            print("Waiting...")
        GPIO.output(19, GPIO.HIGH)
        for c in cmd1:
            bus.write_byte(0x77, ord(c))
            sleep(.01)
        GPIO.output(19, GPIO.LOW)
        return redirect('/')
    if bathiform.validate_on_submit():
        print(bathiform.bathival.data)
        cmd2 = '{"bathi":"'+str(bathiform.bathival.data)+'"}'
        while GPIO.input(26):
            print("Waiting...")
        GPIO.output(19, GPIO.HIGH)
        for c in cmd2:
            bus.write_byte(0x77, ord(c))
            sleep(.01)
        GPIO.output(19, GPIO.LOW)
        return redirect('/')
    if cmdform.validate_on_submit():
        print(cmdform.cmdval.data)
        cmd3 = '{"cmd":"'+str(cmdform.cmdval.data)+'"}'
        #for c in cmd3:
        #    bus.write_byte(0x77, ord(c))
        #    sleep(.01)
        timeout = time.time()+5
        while GPIO.input(26):
            print("Waiting for I2C Bus")
            if time.time() > timeout:
                break
        GPIO.output(19, GPIO.HIGH)
        answer="NaN"
        word = "Empty"
        try:
            #answer = bus.read_i2c_block_data(0x50, 0x00, 16)
            for x in range(0,32):
                answer = eeprom_read_byte(x)
                #word += answer
                print(answer)
            #bus.write_byte(0x50, 0x00)
            #answer = bus.read_byte(0x50)
            #answer = bus.read_byte_data(0x50, 0x00)
            #answer = bus.read_byte(0x77)
            #answer = i2c_msg.read(77,10)
            #bus.i2c_rdwr(answer)
        except:
            print("OOPS!")
        #for value in msg:
        #    print(value)
        print(word)
        GPIO.output(19, GPIO.LOW)
        return redirect('/')
    return render_template('index.html', title='form', batloform=batloform, bathiform=bathiform, cmdform=cmdform)

def eeprom_set_current_address(addr):
    a1=addr/256
    a0=addr%256
    bus.write_i2c_block_data(eepromaddr, a1, [a0])

def eeprom_write_block(addr, data):
    a1=addr/256
    a0=addr%256
    data.insert(0,a0)
    bus.write_i2c_block_data(eepromaddr, a1, data)

def eeprom_read_byte(addr):
    eeprom_set_current_address(addr)
    return bus.read_byte(eepromaddr)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

