import umqtt_robust2, ledring
from machine import Pin
from time import sleep

lib = umqtt_robust2

ledring.color(255, 0, 0)
sleep(10)
ledring.clear()

while True:
    sleep(0.5)
    besked = lib.besked
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        if lib.m == "test":
            lib.client.publish(topic=lib.mqtt_pub_feedname, msg="test tilbage")
            lib.m = ""



    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.client.disconnect()
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
    lib.c.check_msg()
    lib.c.send_queue()
lib.c.disconnect()


