import board
import neopixel
import time
import datetime
import os
import metar

script_dir = os.path.dirname(__file__)
airports_rel_path = 'airports'
airports_abs_path = os.path.join(script_dir, airports_rel_path)
pixels = neopixel.NeoPixel(metar.LED_PIN, metar.LED_COUNT, 0.75, pixel_order = metar.LED_ORDER, auto_write = False)

idx = 0
# turn them all on
for airportcode in airports:
    # Skip NULL entries
    if airportcode == "NULL":
        idx += 1
        continue

    color = metar.COLOR_VFR
    pixels[i] = color
    pixels.show()
    time.sleep(1)
    idx += 1
idx = 0
# now turn them all off
for airportcode in airports:
    # Skip NULL entries
    if airportcode == "NULL":
        idx += 1
        continue

    color = metar.COLOR_CLEAR
    pixels[i] = color
    pixels.show()
    time.sleep(1)
    idx += 1