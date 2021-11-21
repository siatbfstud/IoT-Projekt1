from machine import UART
from micropyGPS import MicropyGPS

def gps_funk():
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    
    #While loop læser data fra gps'en via UART og opdaterer MicropyGPS klassen med værdierne
    while True:
        buf = uart.readline()

        for char in buf:
            gps.update(chr(char))
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]

        #Formaterer data så den er læselig af andre funktioner og Adafruit
        gps_ada = formattedLat+","+formattedLon
        
        if gps.latitude[0] != 0.0:

            print('latitude:', gps.latitude[0])
            print('longitude:', gps.longitude[0])

            return gps_ada



if __name__ == "__gps_funk__":
    print('...running gps_funk, GPS testing')
    gps_funk(False)
