from flask import Flask, request
import RPi.GPIO as GPIO
import gpio_control as GC
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

####################
#    IoT Devices   #
####################
devices = {
    "TV": {
        "power": "off",
        "level": None
    },
    "light": {
        "power": "off",
        "level": None
    },
    "AC": {
        "power": "off",
        "level": 22.0
    },
    "blind": {
        "power": "off",
        "level": 100
    }
}
GC.GPIO_INIT()
####################

def success_response(message):
    return {
        "state": "success",
        "message": message
    }

def fail_response(message):
    return {
        "state": "fail",
        "message": message
    }
def set_AC (val):
    print("In set_AC [%s]"%val)
    try:
        val = float(val)
    except ValueError:
        val = 18.0
    if val < 18.0 : val = 18.0
    elif val > 22.0 : val = 22.0
    devices["AC"]["level"] = val
    if devices["AC"]["power"] == "on" :
        if val <= 19.0 : GC.GPIO_SET("AC", 1)
        elif val <= 20.0 : GC.GPIO_SET("AC", 2)
        elif val <= 21.0 : GC.GPIO_SET("AC", 3)
        else : GC.GPIO_SET("AC", 4)
    else : GC.GPIO_SET("AC", 0)
def set_blind (val):
    print("In set_blind [%s]"%val)
    try:
        val = int(val)
    except ValueError:
        val = 0
    if val < 0 : val = 0
    elif val > 100 : val = 100
    devices["blind"]["level"] = val
    if devices["blind"]["power"] == "on" :
        if val <= 25 : GC.GPIO_SET("blind", 1)
        elif val <= 50 : GC.GPIO_SET("blind", 2)
        elif val <= 75 : GC.GPIO_SET("blind", 3)
        else : GC.GPIO_SET("blind", 4)
    else : GC.GPIO_SET("blind", 0)

def do_operate_GPIO(dtype, oper, value):
    if dtype == "TV" and oper == "power" :
        devices[dtype][oper] = value
        if value == "on" : GC.GPIO_SET(dtype, 1)
        else : GC.GPIO_SET(dtype, 0)
    elif dtype == "light" and oper == "power" :
        devices[dtype][oper] = value
        if value == "on" : GC.GPIO_SET(dtype, 1)
        else : GC.GPIO_SET(dtype, 0)
    
    elif dtype == "AC" and oper == "power" :
        devices[dtype][oper] = value
        if value == "on" : set_AC(devices[dtype]["level"])
        else : GC.GPIO_SET(dtype, 0)
    elif dtype == "AC" and oper == "level" :
        set_AC(value)

    elif dtype == "blind" and oper == "power" :
        devices[dtype][oper] = value
        if value == "on" : set_blind(devices[dtype]["level"])
        else : GC.GPIO_SET(dtype, 0)
    elif dtype == "blind" and oper == "level" :
        set_blind(value)

def operate(type, operation, keys):
    try:
        for k in keys:
            do_operate_GPIO(type, k, operation[k])
        return True
    except KeyError:
        return False

@app.route('/device', methods=['GET'])
def get_status():
    args = request.args
    type = args.get("type")
    try:
        state = devices[type]
        return success_response({"type": type, "state": state})
    except KeyError:
        return fail_response("Unsuportted device")

@app.route('/devices', methods=['POST'])
def operate_devices():
    requests = request.json
    for req in requests:
        try:
            type = req['type']
            operation = req['operation']
            if operate(type, operation, operation.keys()):
                continue
            else:
                return fail_response(f"Fail to operate: {body}")
        except KeyError:
            return fail_response(f"Fail to handle: {body}")
    return success_response(f"Success to operate")

@app.route('/device', methods=['POST'])
def operate_device():
    body = request.json
    try:
        type = body['type']
        operation = body['operation']
        if operate(type, operation, operation.keys()):
            return success_response(f"Success to operate")
        else:
            return fail_response(f"Fail to operate: {body}")
    except KeyError:
        return fail_response(f"Fail to handle: {body}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5555)