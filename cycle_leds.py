import board
import neopixel
import time
import os
LED_COUNT		= 50			# Number of LED pixels.
LED_PIN			= board.D18		# GPIO pin connected to the pixels (18 is PCM).
LED_ORDER		= neopixel.RGB		# Strip type and colour ordering

script_dir = os.path.dirname(__file__)
airports_rel_path = 'airports'
airports_abs_path = os.path.join(script_dir, airports_rel_path)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, 0.75, pixel_order = LED_ORDER, auto_write = False)

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