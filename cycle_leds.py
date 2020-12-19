import board
import neopixel
import time
import os
LED_COUNT		= 50			# Number of LED pixels.
LED_PIN			= board.D18		# GPIO pin connected to the pixels (18 is PCM).
LED_ORDER		= neopixel.RGB		# Strip type and colour ordering

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

color = (255,0,0)
pixels[0] = color
# turn them all on in groups of 10
for multiplier in [1, 2, 3, 4, 5]:
    for idx in [0, 1, 2, 3,4,5,6,7,8]:
        if multiplier is not 1 and idx is not 0:
            pixels[10 * multiplier - 10 + idx] = color
            time.sleep(1)
    # now turn them all off
    for idxi in [0, 1, 2, 3,4,5,6,7,8]::
        if multiplier is not 1 and idx is not 0:
            color = (0,0,0)
            pixels[10 * multiplier - 10 + idxi] = color
