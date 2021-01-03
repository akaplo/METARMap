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
    map_is_on = os.path.exists('mapIsOn')
    if map_is_on:
        return 'Turned on map with mode ' + mode
    else:
        return 'Unable to turn on map'


@server.route('/off', methods=['GET'])
def turn_off():
    map_was_on = os.path.exists('mapIsOn')
    os.system('sudo python3 turn_off.py')
    map_remains_on = os.path.exists('mapIsOn')
    if map_was_on and map_remains_on:
        return 'Unable to turn off map'
    elif map_was_on:
        return 'Turned off map'
    else:
        return 'Map was not on'


@server.route('/status')
def status():
    statefile_exists = os.path.exists('mapIsOn')
    return 'The map is ' + 'ON' if statefile_exists else 'OFF'
