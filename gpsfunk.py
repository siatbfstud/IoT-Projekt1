from machine import UART
from time import sleep
from micropyGPS import MicropyGPS
import geofence, PlayerClass


player = PlayerClass.Player(0,0)


def gps_funk():
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    
    while True:
        buf = uart.readline()

        for char in buf:
            gps.update(chr(char))
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]
        formattedAlt = str(gps.altitude)
        formattedSpd = gps.speed_string()
        formattedSpd = formattedSpd[:-5]

        
        gps_ada = formattedSpd+","+formattedLat+","+formattedLon+","+formattedAlt
        
        if gps.latitude[0] != 0.0:
            
            player.lat = gps.latitude[0]
            player.lon = gps.longitude[0]


            print('latitude:', gps.latitude[0])
            print('longitude:', gps.longitude[0])

            return gps_ada



if __name__ == "__gps_funk__":
    print('...running gps_funk, GPS testing')
    gps_funk(False)
