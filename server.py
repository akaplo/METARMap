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
    statefile = open('ledsOn', 'w')
    statefile.close()
    return 'Turned on map with mode ' + mode


@server.route('/off', methods=['GET'])
def turn_off():
    os.system('sudo python3 turn_off.py')
    if os.path.exists('ledsOn'):
        os.remove('ledsOn')
        return 'Turned off map'
    else:
        return 'Map was not on (or, at least, indicator file did not exist)'


@server.route('/status')
def status():
    statefile_exists = os.path.exists('ledsOn')
    return 'The map is ' + 'ON' if statefile_exists else 'OFF (or, at least, indicator file does not exist)'
