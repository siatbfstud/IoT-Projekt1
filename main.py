import umqtt_robust2, gpsfunk, mpu6050, geofence
from machine import Pin, I2C
from time import sleep

lib = umqtt_robust2
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'map/csv'), 'utf-8')
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'speed/csv'), 'utf-8')
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq = 10000)
mpu= mpu6050.accel(i2c)

while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        lib.c.publish(topic=mapFeed, msg=gpsfunk.gps_funk())
        

        
        #Gyroskop
        mpu.get_values()
        print(mpu.get_values())
        
        #Gps hastighed
        speed = gpsfunk.gps_funk()
        speed = speed[:4]
        #print("speed: ",speed)
        lib.c.publish(topic=speedFeed, msg=speed)
        sleep(10) 

    except KeyboardInterrupt:
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