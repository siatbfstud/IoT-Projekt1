import umqtt_robust2, led_ring_controller, geofence
from machine import Pin
from utime import sleep
import _thread as t
from gpsfunk import gps_funk

#Definerer vibrator og MQTT
vib = Pin(19, Pin.OUT, value = 0)
lib = umqtt_robust2

#Definerer globale variabler
stopmeGPS = False
stopmeIndicator = False
gps_ada = str()
running = False

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

#Thread til GPS
def thread_GPS(): 
    global stopmeGPS
    while stopmeGPS is False:
        try:
            global gps_ada
            global latLon
            gps_ada = gps_funk()
            #Laver liste ud af gps_ada
            latLon = gps_ada.split(",")
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
        #Starter thread til LED Bounce funktion, virker ikke nu da hardware har problemer.
        t.start_new_thread(led_ring_controller.bounce,(50,0,0,100))
        vib.value(1)
        send_data_info("1")
        send_debug_info("Ude af zonen")
        return False

def zone_picker(nr):
    geofence.zone_setup(nr)
    sleep(3)
    return

#Main loop
while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        #Hvis toggle knap på Adafruit er tændt
        if lib.besked == "1":
            stopmeIndicator = False
            stopmeGPS = False
            running = True
            t.start_new_thread(thread_GPS,())
            print("hello")
            lib.besked = ""
            sleep(2)
        #Running er en global variable styret af toggle fra Adafruit
        if running is True:
            print("in main loop, numBesked:", lib.numBesked)
            #Tjekker numpad værdi fra Adafruit, og sender den videre til zonepicker funktionen
            if lib.numBesked != "":
                zone_picker(int(lib.numBesked))
                t.start_new_thread(thread_indicator,())
                lib.numBesked = ""
                print("Exiting zonepicker if statement")

            lib.c.check_msg()
            lib.c.send_queue()
            #Hvis toggle knap er slukket
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
            send_debug_info("Not Running")
        sleep(5) 

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