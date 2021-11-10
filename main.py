import umqtt_robust2
import GPSfunk
from machine import Pin
from time import sleep_ms, sleep

lib = umqtt_robust2
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'map/csv'), 'utf-8')
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'siatbf', b'speed/csv'), 'utf-8')

while True:
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        lib.c.publish(topic=mapFeed, msg=GPSfunk.gps_funk())
        speed = GPSfunk.gps_funk()
        speed = speed[:4]
        print("speed: ",speed)
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