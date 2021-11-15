import umqtt_robust2, gpsfunk, geofence, led_ring_controller
from machine import Pin, SoftI2C
from time import gmtime, localtime, sleep
import hmc5883l
import _thread as t
import ntptime


vib = Pin(19, Pin.OUT, value = 0)
lib = umqtt_robust2
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.map/csv'), 'utf-8')
indicatorFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.indicator/csv'), 'utf-8')
toggleFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'bot_sub/csv'), 'utf-8')
debugFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'iotfeed.debug/csv'), 'utf-8')

running = False

ntptime.settime()

""" 

TO DO 
Start og stop Funktion DONE

Når spiller forlader zone
1. Tænd vibrator DONE
2. Tænd LED ring
3. Ude af zone starttid til graf og tid brugt ude.

Send 0 til indikator ADA, ved slut DONE

Vesten bliver taget på og er ikke tændt selvom den er sluttet til strøm. DONE

HVIS VI HAVDE MERE TID:
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

def send_debug_info(string):
    lib.c.publish(topic=debugFeed, msg=string)

def get_time():
    print(localtime())

while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        if lib.besked == "1":
            running = True
        else:
            print("Not Running")
            running = False
        while running:
            
            get_time()

            t.start_new_thread(lib.c.publish,(mapFeed,gpsfunk.gps_funk(False)))
            #lib.c.publish(topic=mapFeed, msg=gpsfunk.gps_funk(False))
            
            #lib.c.publish(topic=indicatorFeed, msg=str(gpsfunk.gps_funk(True)))
            t.start_new_thread(lib.c.publish,(indicatorFeed,str(gpsfunk.gps_funk(True))))
            
            #Gyroskop
            #imu = MPU6050(SoftI2C(scl=Pin(22), sda=Pin(21)))
            #print(imu.mag.xyz)
            
            lib.c.check_msg()
            lib.c.send_queue()
            if lib.besked == "0":
                running = False
            sleep(2)
        sleep(2) 

    except KeyboardInterrupt:
        lib.c.publish(topic=indicatorFeed, msg="0")
        lib.c.publish(topic=toggleFeed, msg="0")
        print('Ctrl-C pressed...exiting')
        vib.value(0)
        sleep(3)
        led_ring_controller.clear()
        lib.c.disconnect()
        lib.wifi.active(False)
        lib.sys.exit()
    except OSError as e:
        print(e)
    except NameError as e:
        print(e)
    except TypeError as e:
        print(e)
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages

lib.c.disconnect()