from machine import UART
from time import sleep
from micropyGPS import MicropyGPS
import geofence, PlayerClass


player = PlayerClass.Player(0,0)


def gps_funk(testZone:bool):
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
        
        if gps.latitude[0] != 0.0 and testZone == False:
            
            player.lat = gps.latitude[0]
            player.lon = gps.longitude[0]

            """RUN ONCE PLS FIX"""
            #RETURN GPS FUNK TIL MAIN; OG KØR ZONE SETUP DERFRA
            geofence.zone_setup(player.lat,player.lon)


            print('latitude:', gps.latitude[0])
            print('longitude:', gps.longitude[0])

            sleep(5)
            return gps_ada

        if testZone == True:
            return int(geofence.testzone(player.lat,player.lon))


if __name__ == "__gps_funk__":
    print('...running gps_funk, GPS testing')
    gps_funk(False)
