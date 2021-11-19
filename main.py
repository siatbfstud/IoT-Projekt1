import umqtt_robust2, led_ring_controller, geofence
from machine import Pin
from utime import sleep
import _thread as t
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

#Sender data til Adafruit, så man kan debug og sende data uden en terminal på PC'en
def send_debug_info(string):
    lib.c.publish(topic=debugFeed, msg=string)

def send_data_info(string):
    lib.c.publish(topic=dataFeed, msg=string)

def thread_GPS(): 
    global stopmeGPS
    while stopmeGPS is False:
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
    if stopmeGPS is True:
        print("Exiting GPS THREAD")
        t.exit()

def thread_indicator():
    global stopmeIndicator
    while stopmeIndicator == False:
        try:
            global latLon
            print (latLon)
            #Tjekker hvad indikator value er, og publisher til Adafruit
            indicatorBool = int(testzone(float(latLon[0]),float(latLon[1])))
            lib.c.publish(indicatorFeed,str(indicatorBool))
            sleep(5)
        except Exception as e:
            print("INDICATOR THREAD DIED:", e)
            t.exit()
    if stopmeIndicator is True:
        print("Exiting Indicator Thread")
        t.exit()

def testzone(lat, lon):
    #global stopmeGPS
    #Hvis spillerene er inde for zonen
    if geofence.my_fence.check_point((lat, lon)) == True:
        print("Inde i zonen")
        send_data_info("0")
        send_debug_info("Inde i zonen")
        led_ring_controller.clear()
        vib.value(0)
        return True
    #Hvis spilleren er ude for zonen
    else:
        print("Ude af zonen")
        #stopmeGPS = True
        #sleep(10)
        #t.start_new_thread(led_ring_controller.bounce,(50,0,0,100))
        #sleep(10)
        #stopmeGPS = False
        #t.start_new_thread(thread_GPS,())
        vib.value(1)
        send_data_info("1")
        send_debug_info("Ude af zonen")
        return False


def zone_picker(nr):
    geofence.zone_setup(nr)
    sleep(3)
    return

stopmeGPS = False
stopmeIndicator = False
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
            print("hello")
            lib.besked = ""
            sleep(5)
        if running is True:    
            print("in main loop, numBesked:", lib.numBesked)

            if lib.numBesked != "":
                zone_picker(int(lib.numBesked))
                print(stopmeIndicator)
                t.start_new_thread(thread_indicator,())
                lib.numBesked = ""
                print("Exiting zonepicker if statement")

            lib.c.check_msg()
            lib.c.send_queue()
            if lib.besked == "0":
                running = False
                stopmeIndicator = True
                stopmeGPS = True
                vib.value(0)
                led_ring_controller.clear()
                lib.c.publish(topic=indicatorFeed, msg="0")
            sleep(2)
        else:
            print("Not Running")
            send_debug_info("Not Runnig")
        sleep(10) 

    except KeyboardInterrupt:
        #Reset alle komponeneter og alt på adafruit når main loop lukkes
        stopmeIndicator = True
        stopmeGPS = True
        lib.c.publish(topic=indicatorFeed, msg="0")
        lib.c.publish(topic=toggleFeed, msg="0")
        print('Ctrl-C pressed...exiting')
        vib.value(0)
        led_ring_controller.clear()
        sleep(5)
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