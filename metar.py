import urllib.request
import xml.etree.ElementTree as ET
import board
import neopixel
import time
import datetime
import os
import random

# metar.py script iteration 1.4.1

# ---------------------------------------------------------------------------
# ------------START OF CONFIGURATION-----------------------------------------
# ---------------------------------------------------------------------------

# NeoPixel LED Configuration
LED_COUNT		= 50			# Number of LED pixels.
LED_PIN			= board.D18		# GPIO pin connected to the pixels (18 is PCM).
LED_BRIGHTNESS		= 0.5			# Float from 0.0 (min) to 1.0 (max)
LED_ORDER		= neopixel.RGB		# Strip type and colour ordering

COLOR_VFR		= (255,0,0)		# Green
COLOR_VFR_FADE		= (125,0,0)		# Green Fade for wind
COLOR_MVFR		= (0,0,255)		# Blue
COLOR_MVFR_FADE		= (0,0,125)		# Blue Fade for wind
COLOR_IFR		= (0,255,0)		# Red
COLOR_IFR_FADE		= (0,125,0)		# Red Fade for wind
COLOR_LIFR		= (0,125,125)		# Magenta
COLOR_LIFR_FADE		= (0,75,75)		# Magenta Fade for wind
COLOR_CLEAR		= (0,0,0)		# Clear
COLOR_LIGHTNING		= (255,255,255)		# White

# ----- Blink/Fade functionality for Wind and Lightning -----
# Do you want the METARMap to be static to just show flight conditions, or do you also want blinking/fading based on current wind conditions
ACTIVATE_WINDCONDITION_ANIMATION = False	# Set this to False for Static or True for animated wind conditions
#Do you want the Map to Flash white for lightning in the area
ACTIVATE_LIGHTNING_ANIMATION = False		# Set this to False for Static or True for animated Lightning
# Fade instead of blink
FADE_INSTEAD_OF_BLINK	= True			# Set to False if you want blinking
# Blinking Windspeed Threshold
WIND_BLINK_THRESHOLD	= 15			# Knots of windspeed
ALWAYS_BLINK_FOR_GUSTS	= False			# Always animate for Gusts (regardless of speeds)
# Blinking Speed in seconds
BLINK_SPEED		= 1.0			# Float in seconds, e.g. 0.5 for half a second
# Total blinking time in seconds.
# For example set this to 300 to keep blinking for 5 minutes if you plan to run the script every 5 minutes to fetch the updated weather
BLINK_TOTALTIME_SECONDS	= 300

# ----- Daytime dimming of LEDs based on time of day or Sunset/Sunrise -----
ACTIVATE_DAYTIME_DIMMING = False		# Set to True if you want to dim the map after a certain time of day
BRIGHT_TIME_START	= datetime.time(7,0)	# Time of day to run at LED_BRIGHTNESS in hours and minutes
DIM_TIME_START		= datetime.time(19,0)	# Time of day to run at LED_BRIGHTNESS_DIM in hours and minutes
LED_BRIGHTNESS_DIM	= 0.1			# Float from 0.0 (min) to 1.0 (max)

USE_SUNRISE_SUNSET 	= True			# Set to True if instead of fixed times for bright/dimming, you want to use local sunrise/sunset
LOCATION 		= "Boston"		# Nearby city for Sunset/Sunrise timing, refer to https://astral.readthedocs.io/en/latest/#cities for list of cities supported

# ---------------------------------------------------------------------------
# ------------END OF CONFIGURATION-------------------------------------------
# ---------------------------------------------------------------------------


def suppress_some_leds(leds):
    indices = [random.randrange(0, 47) for i in range(10)]
    print(str(indices))
    i = 0
    for led in leds:
        if i not in indices:
            leds[i] = (0,0,0)
        i += 1
    return leds

def clear(pixels):
    for i in range(50):
        pixels[i] = (0,0,0)
    pixels.show()
    return pixels

def run():
    # Initialize the LED strip
    print("Running metar.py at " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))
    script_dir = os.path.dirname(__file__)
    airports_rel_path = 'airports'
    airports_abs_path = os.path.join(script_dir, airports_rel_path)
    bright = BRIGHT_TIME_START < datetime.datetime.now().time() < DIM_TIME_START
    print("Wind animation:" + str(ACTIVATE_WINDCONDITION_ANIMATION))
    print("Lightning animation:" + str(ACTIVATE_LIGHTNING_ANIMATION))
    print("Daytime Dimming:" + str(ACTIVATE_DAYTIME_DIMMING) + (" using Sunrise/Sunset" if USE_SUNRISE_SUNSET and ACTIVATE_DAYTIME_DIMMING else ""))
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS_DIM if (ACTIVATE_DAYTIME_DIMMING and bright == False) else LED_BRIGHTNESS, pixel_order = LED_ORDER, auto_write = False)

    # Read the airports file to retrieve list of airports and use as order for LEDs
    with open(airports_abs_path) as f:
        airports = f.readlines()
    airports = [x.strip() for x in airports]

    # Retrieve METAR from aviationweather.gov data server
    # Details about parameters can be found here: https://www.aviationweather.gov/dataserver/example?datatype=metar
    url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
    print(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'})
    content = urllib.request.urlopen(req).read()

    # Retrieve flying conditions from the service response and store in a dictionary for each airport
    root = ET.fromstring(content)
    conditionDict = { "NULL": {"flightCategory" : "", "windDir": "", "windSpeed" : 0, "windGustSpeed" :  0, "windGust" : False, "lightning": False, "tempC" : 0, "dewpointC" : 0, "vis" : 0, "altimHg" : 0, "obs" : "", "skyConditions" : {}, "obsTime" : datetime.datetime.now() } }
    conditionDict.pop("NULL")
    stationList = []
    for metar in root.iter('METAR'):
        stationId = metar.find('station_id').text
        if metar.find('flight_category') is None:
            print("Missing flight condition, skipping.")
            continue
        flightCategory = metar.find('flight_category').text
        windDir = ""
        windSpeed = 0
        windGustSpeed = 0
        windGust = False
        lightning = False
        tempC = 0
        dewpointC = 0
        vis = 0
        altimHg = 0.0
        obs = ""
        skyConditions = []
        if metar.find('wind_gust_kt') is not None:
            windGustSpeed = int(metar.find('wind_gust_kt').text)
            windGust = (True if (ALWAYS_BLINK_FOR_GUSTS or windGustSpeed > WIND_BLINK_THRESHOLD) else False)
        if metar.find('wind_speed_kt') is not None:
            windSpeed = int(metar.find('wind_speed_kt').text)
        if metar.find('wind_dir_degrees') is not None:
            windDir = metar.find('wind_dir_degrees').text
        if metar.find('temp_c') is not None:
            tempC = int(round(float(metar.find('temp_c').text)))
        if metar.find('dewpoint_c') is not None:
            dewpointC = int(round(float(metar.find('dewpoint_c').text)))
        if metar.find('visibility_statute_mi') is not None:
            vis = int(round(float(metar.find('visibility_statute_mi').text)))
        if metar.find('altim_in_hg') is not None:
            altimHg = float(round(float(metar.find('altim_in_hg').text), 2))
        if metar.find('wx_string') is not None:
            obs = metar.find('wx_string').text
        if metar.find('observation_time') is not None:
            obsTime = datetime.datetime.fromisoformat(metar.find('observation_time').text.replace("Z","+00:00"))
        for skyIter in metar.iter("sky_condition"):
            skyCond = { "cover" : skyIter.get("sky_cover"), "cloudBaseFt": int(skyIter.get("cloud_base_ft_agl", default=0)) }
            skyConditions.append(skyCond)
        if metar.find('raw_text') is not None:
            rawText = metar.find('raw_text').text
            lightning = False if rawText.find('LTG') == -1 else True
        print(stationId + ":"
        + flightCategory + ":"
        + str(windDir) + "@" + str(windSpeed) + ("G" + str(windGustSpeed) if windGust else "") + ":"
        + str(vis) + "SM:"
        + obs + ":"
        + str(tempC) + "/"
        + str(dewpointC) + ":"
        + str(altimHg) + ":"
        + str(lightning))
        conditionDict[stationId] = { "flightCategory" : flightCategory, "windDir": windDir, "windSpeed" : windSpeed, "windGustSpeed": windGustSpeed, "windGust": windGust, "vis": vis, "obs" : obs, "tempC" : tempC, "dewpointC" : dewpointC, "altimHg" : altimHg, "lightning": lightning, "skyConditions" : skyConditions, "obsTime": obsTime }
        stationList.append(stationId)

    # Setting LED colors based on weather conditions
    looplimit = int(round(BLINK_TOTALTIME_SECONDS / BLINK_SPEED)) if (ACTIVATE_WINDCONDITION_ANIMATION or ACTIVATE_LIGHTNING_ANIMATION) else 1

    windCycle = False
    numAirports = len(stationList)
    pixels = clear(pixels)
    while looplimit > 0:
        i = 0
        for airportcode in airports:
            # Skip NULL entries
            if airportcode == "NULL":
                i += 1
                continue

            color = COLOR_CLEAR
            conditions = conditionDict.get(airportcode, None)
            windy = False
            lightningConditions = False

            if conditions != None:
                windy = True if (ACTIVATE_WINDCONDITION_ANIMATION and windCycle == True and (conditions["windSpeed"] > WIND_BLINK_THRESHOLD or conditions["windGust"] == True)) else False
                lightningConditions = True if (ACTIVATE_LIGHTNING_ANIMATION and windCycle == False and conditions["lightning"] == True) else False
                if conditions["flightCategory"] == "VFR":
                    color = COLOR_VFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else (COLOR_VFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "MVFR":
                    color = COLOR_MVFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else (COLOR_MVFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "IFR":
                    color = COLOR_IFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else (COLOR_IFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "LIFR":
                    color = COLOR_LIFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else (COLOR_LIFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                else:
                    color = COLOR_CLEAR

            print("Setting LED " + str(i) + " for " + airportcode + " to " + ("lightning " if lightningConditions else "") + ("windy " if windy else "") + (conditions["flightCategory"] if conditions != None else "None") + " " + str(color))
            pixels[i] = color
            i += 1

        # Update actual LEDs all at once
        pixels = suppress_some_leds(pixels)
        print(str(pixels))
        pixels.show()

        # Switching between animation cycles
        time.sleep(BLINK_SPEED)
        windCycle = False if windCycle else True
        looplimit -= 1

    print()
    print("Done")
