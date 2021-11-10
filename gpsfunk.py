from machine import UART
from micropyGPS import MicropyGPS
import geofence

def gps_funk():
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
        
        if gps.latitude[0] != 0.0:
            #print("gps_ada: ",gps_ada)
            print('latitude:', gps.latitude[0])
            print('longitude:', gps.longitude[0])
            geofence.testzone(gps.latitude[0], gps.longitude[0])
            return gps_ada
if __name__ == "__gps_funk__":
    print('...running gps_funk, GPS testing')
    gps_funk()
