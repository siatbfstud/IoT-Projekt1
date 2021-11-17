import picket
import haversine
import PlayerClass
import json, io
import led_ring_controller
from machine import Pin
import _thread as t

vib = Pin(19, Pin.OUT, value = 0)

my_fence = picket.Fence()

def zone_setup(lat:float,lon:float):
    import main
    #Disse tre linjer skaber 2 af de 4 hjørner, i koordinater, til en zone, putter dem i en Zone Class.
    #Tredje linje udregner de resterende hjørner, og kan derefter bruges af picket
    newZone = haversine.makeZone([lat,lon],8,2)
    newZone = PlayerClass.Zone(newZone[0], newZone[1])
    newZoneBorders = newZone.calculate_borders(newZone.nwBorder, newZone.seBorder)
    #Finder heading fra magnetometer
    newZone.get_heading()
    
    if main.lib.c.publish(topic=main.zonePickerFeed, msg="0"):
        with io.open("zones.json") as o:
            zone1 = json.loads(o)
            print(zone1)

    #Ude af zonen
    my_fence.add_point((55.707020, 12.537976))
    my_fence.add_point((55.707026, 12.537022))
    my_fence.add_point((55.707507, 12.537038))
    my_fence.add_point((55.707581, 12.538344))


def testzone(lat, lon):
    import main

    #Hvis spillerene er inde for zonen
    if my_fence.check_point((lat, lon)) == True:
        print("Inde i zonen")
        main.send_data_info("0")
        main.send_debug_info("Inde i zonen")
        led_ring_controller.clear()
        vib.value(0)
        return True
    #Hvis spilleren er ude for zonen
    else:
        print("Ude af zonen")
        #t.start_new_thread(led_ring_controller.bounce,(50,0,0,100))
        print("after LED call")
        vib.value(1)
        main.send_data_info("1")
        main.send_debug_info("Ude af zonen")
        return False
