import neopixel
from machine import Pin
from time import sleep_ms
 
np = neopixel.NeoPixel(Pin(17),12)

def color(r, g, b):
    for i in range(12):
        np[i] = (r, g, b)
    np.write()


def bounce(r, g, b, wait):
    for i in range (12):
        np[i] = (r, g, b)
    np.write()
    sleep_ms(wait)

def clear():
    for i in range(12):
        np[i] = (0, 0, 0)
        np.write() 