import neopixel
from machine import Pin
from time import sleep_ms

n = 12

np = neopixel.NeoPixel(Pin(17),n)

def color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()


def bounce(r, g, b, wait):
    #while on:
    for i in range(n):
        print("Loop",i)
        np[i] = (r,g,b)
        np[i-1] = (r,g,b)
        np[i-2] = (r,g,b)
        np.write()
        sleep_ms(wait)
        clear() 

def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()

