from flask import Flask, render_template, redirect
from flask import request
from time import sleep
from forms import BatLoForm, BatHiForm, CmdForm
import time
import smbus

bus = smbus.SMBus(3)

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
        for c in cmd1:
            bus.write_byte(0x77, ord(c))
            sleep(.01)
        return redirect('/')
    if bathiform.validate_on_submit():
        print(bathiform.bathival.data)
        cmd2 = '{"bathi":"'+str(bathiform.bathival.data)+'"}'
        for c in cmd2:
            bus.write_byte(0x77, ord(c))
            sleep(.01)
        return redirect('/')
    if cmdform.validate_on_submit():
        print(cmdform.cmdval.data)
        cmd3 = '{"cmd":"'+str(cmdform.cmdval.data)+'"}'
        for c in cmd3:
            bus.write_byte(0x77, ord(c))
            sleep(.01)
        return redirect('/')
    return render_template('index.html', title='form', batloform=batloform, bathiform=bathiform, cmdform=cmdform)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
