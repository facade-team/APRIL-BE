from flask import Flask, request

app = Flask(__name__)

####################
#    Mocking IoT   #
####################
devices = {
    "TV": {
        "power": "off",
        "level": None,
    },
    "light": {
        "power": "off",
        "level": None,
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
def operate(type, operation, keys):
    try:
        for k in keys:
            devices[type][k] = operation[k]
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
    app.run(debug=True, port=5555)