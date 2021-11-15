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

        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites:', gps.satellites_in_use)
        #print('Altitude:', gps.altitude)
        #print('latitude:', gps.latitude_string())
        #print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]
        formattedAlt = str(gps.altitude)
        formattedSpd = gps.speed_string()
        formattedSpd = formattedSpd[:-5]

        
        gps_ada = formattedSpd+","+formattedLat+","+formattedLon+","+formattedAlt
        # def startGPSthread():
        # _thread.start_new_thread(main, ())

        if gps.latitude[0] != 0.0 and testZone == False:
            
            player.lat = gps.latitude[0]
            player.lon = gps.longitude[0]

            """RUN ONCE PLS FIX"""
            geofence.zone_setup(player.lat,player.lon)



            #print("gps_ada: ",gps_ada)
            print('latitude:', gps.latitude[0])
            print('longitude:', gps.longitude[0])
            #geofence.testzone(gps.latitude[0], gps.longitude[0])
            sleep(5)
            return gps_ada

        if testZone == True:
            #print(player.lat,player.lon)
            #sleep(2)
            return int(geofence.testzone(player.lat,player.lon))


if __name__ == "__gps_funk__":
    print('...running gps_funk, GPS testing')
    gps_funk(False)
