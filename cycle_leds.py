import board
import neopixel
import time
import os
LED_COUNT		= 50			# Number of LED pixels.
LED_PIN			= board.D18		# GPIO pin connected to the pixels (18 is PCM).
LED_ORDER		= neopixel.RGB		# Strip type and colour ordering
LED_BRIGHTNESS = 0.5
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS)

color_red = (255,0,0)
color_clear = (0,0,0)
pixels[0] = color_red
# turn them all on in groups of 10
for multiplier in [1, 2, 3, 4, 5]:
    for idx in [0, 1, 2, 3,4,5,6,7,8]:
        p = 10 * multiplier - 10 + idx
        if (multiplier + idx != 1):
            print("turning on " + str(p))
            pixels[p] = color_red
            time.sleep(1)
    # now turn them all off
    for idxi in [0, 1, 2, 3,4,5,6,7,8]:
        if (multiplier + idxi != 1):
            p = 10 * multiplier - 10 + idxi
            print("turning off " + str(p))
            pixels[p] = color_clear
pixels.deinit()