from flask import Flask, request
import os
from metar import map_modes

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
    body = request.get_json()
    mode = body['mode']
    if mode not in map_modes.values():
        return 'Invalid mode: expected one of ' + str(map_modes.values()) + ' but got ' + mode
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
    state = None
    if statefile_exists:
        file = open('mapIsOn', 'r')
        state = file.readline()
        file.close()
    return {
        'map_is_on': statefile_exists,
        'mode': state if state is not None else None
    }
