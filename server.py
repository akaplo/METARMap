from flask import Flask, request
import os

server = Flask(__name__)


@server.route('/', methods=['GET'])
def index():
    return 'MeteroLEDgy'


# Body:
# {
#   'mode': string - The desired map mode. One of ['temp', 'conditions', 'cycle']
# }
@server.route('/on', methods=['POST'])
def turn_on():
    allowed_modes = ['temp', 'conditions']
    body = request.get_json()
    print(body)
    mode = body['mode']
    if mode not in allowed_modes:
        return 'Invalid mode: expected one of ' + str(allowed_modes) + ' but got ' + mode
    os.system('sudo python3 metar.py ' + mode)
    return 'Turned on map with mode ' + mode


@server.route('/off', methods=['GET'])
def turn_off():
    return 'Turned off map'


@server.route('/status')
def status():
    return 'Not yet implemented'
