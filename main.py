import umqtt_robust2, led_ring_controller, geofence
from machine import Pin
from time import gmtime, localtime, sleep
import _thread as t
import ntptime
from gpsfunk import gps_funk

vib = Pin(19, Pin.OUT, value = 0)
lib = umqtt_robust2

#Forskellige feeds til Adafruit IO
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.map/csv'), 'utf-8')
indicatorFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.indicator/csv'), 'utf-8')
toggleFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'bot_sub/csv'), 'utf-8')
debugFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.debug/csv'), 'utf-8')
dataFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.data/csv'), 'utf-8')
numsubFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'numsub/csv'), 'utf-8')


#Sætter RTC på ESP32 til nuværende tid, trukket fra en pool på nettet. (pool.ntp.org)
#ntptime.settime()

#Sender data til Adafruit, så man kan debug og sende data uden en terminal på PC'en
def send_debug_info(string):
    lib.c.publish(topic=debugFeed, msg=string)

def send_data_info(string):
    lib.c.publish(topic=dataFeed, msg=string)

#Return nuværende tidspunkt i en tuple
def get_time():
    return localtime()

def thread_GPS(): 
    global stopme
    if stopme is True:
        t.exit()
    try:
        global gps_ada
        global latLon
        gps_ada = gps_funk()
        latLon = gps_ada.rsplit(",")
        #Publisher til adafruit map
        lib.c.publish(mapFeed,"0.0,"+gps_ada+",0.0")
        sleep(5)
    except Exception as e:
        print("GPS THREAD DIED:", e)
        t.exit()

def thread_indicator():
    try:
        global latLon
        print (latLon)
        #Tjekker hvad indikator value er, og publisher til Adafruit
        indicatorBool = int(geofence.testzone(float(latLon[0]),float(latLon[1])))
        lib.c.publish(indicatorFeed,str(indicatorBool))
        sleep(5)
    except Exception as e:
        print("INDICATOR THREAD DIED:", e)
        t.exit()

def zone_picker(nr):
    global latLon
    geofence.zone_setup(float(latLon[0]), float(latLon[1]),nr)
    sleep(3)
    t.start_new_thread(thread_indicator,())
    return

stopme = False
gps_ada = str()
running = False
#Main loop
while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        if lib.besked == "1":
            running = True
            t.start_new_thread(thread_GPS,())
            sleep(5)
        else:
            print("Not Running")
        if running is True:
            get_time()      
            print("in main loop, numBesked:", lib.numBesked)

            if lib.numBesked != "":
                zone_picker(int(lib.numBesked))
                lib.numBesked = ""
                print("Exiting zonepicker if statement")
            
            lib.c.check_msg()
            lib.c.send_queue()
            if lib.besked == "0":
                running = False
                vib.value(0)
                led_ring_controller.clear()
                lib.c.publish(topic=indicatorFeed, msg="0")
            sleep(2)
        sleep(2) 

    except KeyboardInterrupt:
        #Reset alle komponeneter og alt på adafruit når main loop lukkes
        lib.c.publish(topic=indicatorFeed, msg="0")
        lib.c.publish(topic=toggleFeed, msg="0")
        print('Ctrl-C pressed...exiting')
        vib.value(0)
        led_ring_controller.clear()
        sleep(3)
        lib.c.disconnect()
        lib.wifi.active(False)
        lib.sys.exit()
    except OSError as e:
        print(e)
    except NameError as e:
        print(e)
    except TypeError as e:
        print(e)
    lib.c.check_msg()
    lib.c.send_queue()

lib.c.disconnect()



""" 
Filer vi skal kende:
boot.py
main.py
geofence.py
gpfunk.py
haversine.py
led_ring_controller.py
PlayerClass.py


TO DO
Tænd LED ring når spiller forlader zone
Ude af zone starttid til graf og tid brugt ude

Processen:
 - Self generated zones uden knap - 
    Spilleren stiller sig i midten af den zone han skal spille i og vender sig mod et mål.
    Træner/hjælpetræner kan på adafruit vælge zonens bredde og længde som bliver genereret ud fra spillerens position og retning og aktiverer den. 
    Træneren vælger på adafruit når zonen skal være inaktiv og træningen er ovre


 - Pre defined zones med knap - 
    Spilleren stiller sig et sted i sin zone der er defineret og valgt i adafruit. 
    Når spilleren er ude af zonen bliver data sendt til adafruit med tidspunkter.
    

Når spilleren er ude fra zonen, bouncer LED-ring rødt og vibrator tænder. 
Samtidig ændrer Zone-indicatoren på adafruit til rød og et timestamp, samt hvor lang tid personen var ude af zonen sendt til adafruit.

Når en zone "lukkes", bliver data timestamp og tid ude fra zonen lagt på et feed som spilleren kan se efter træning.
"""