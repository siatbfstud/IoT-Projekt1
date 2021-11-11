import umqtt_robust2, gpsfunk, mpu6050, geofence
from machine import Pin, I2C
from time import sleep

lib = umqtt_robust2
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'map/csv'), 'utf-8')
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'speed/csv'), 'utf-8')
zoneFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'zone/csv'), 'utf-8')
i2c = I2C(scl=Pin(22), sda=Pin(21), freq = 10000)
mpu= mpu6050.accel(i2c)


""" 

TO DO 
Start og stop Funktion

Når spiller forlader zone
1. Tænd vibrator
2. Tænd LED ring
3. Ude af zone starttid og tid brugt ude.

Send 0 til indikator ADA, ved slut


"""



while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        lib.c.publish(topic=mapFeed, msg=gpsfunk.gps_funk(False))
        print(gpsfunk.gps_funk(True))
        
        lib.c.publish(topic=zoneFeed, msg=str(gpsfunk.gps_funk(True)))

        
        #Gyroskop
        mpu.get_values()
        print(mpu.get_values())
        
        #Gps hastighed
        #speed = gpsfunk.gps_funk(False)
        #speed = speed[:4]
        #print("speed: ",speed)
        #lib.c.publish(topic=speedFeed, msg=speed)
        sleep(10) 

    except KeyboardInterrupt:
        lib.c.publish(topic=zoneFeed, msg="0")
        print('Ctrl-C pressed...exiting')
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