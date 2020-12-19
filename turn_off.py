
import board
import neopixel
import time
import os
LED_COUNT               = 50                    # Number of LED pixels.
LED_PIN                 = board.D18             # GPIO pin connected to the pixels (18 is PCM).
LED_ORDER               = neopixel.RGB          # Strip type and colour ordering

#script_dir = os.path.dirname(__file__)
#airports_rel_path = 'airports'
#airports_abs_path = os.path.join(script_dir, airports_rel_path)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

# now turn them all off
for idxi in range(50):
    color = (0,0,0)
    pixels[idxi] = color


