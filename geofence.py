import picket
import haversine
import PlayerClass
import led_ring_controller
from machine import Pin
import _thread as t

vib = Pin(19, Pin.OUT, value = 0)

my_fence = picket.Fence()

def zone_setup(lat,lon):
    mkzoneRes = haversine.makeZone([lat,lon],8,2)
    tempZone = PlayerClass.Zone(mkzoneRes[0], mkzoneRes[1])
    borders = tempZone.calculate_borders(tempZone.nwBorder, tempZone.seBorder)
    
    #my_fence.add_point((55.706677, 12.538627))
    #my_fence.add_point((55.706165, 12.538455))
    #my_fence.add_point((55.705993, 12.540409))
    #my_fence.add_point((55.706570, 12.540522))

    my_fence.add_point((55.707020, 12.537976))
    my_fence.add_point((55.707026, 12.537022))
    my_fence.add_point((55.707507, 12.537038))
    my_fence.add_point((55.707581, 12.538344))


def testzone(lat, lon):
    import main
    #Inde i zone
    #my_fence.add_point((55.706677, 12.538627))
    #my_fence.add_point((55.706165, 12.538455))
    #my_fence.add_point((55.705993, 12.540409))
    #my_fence.add_point((55.706570, 12.540522))
    
    """ ZONE SKIFTER VED HVER OPDATERING, FIKS DET"""
    

    #Ude af zone
#     my_fence.add_point((55.707020, 12.537976))
#     my_fence.add_point((55.707026, 12.537022))
#     my_fence.add_point((55.707507, 12.537038))
#     my_fence.add_point((55.707581, 12.538344))

    if my_fence.check_point((lat, lon)) == True:
        print("Inde i zonen")
        main.send_debug_info("Inde i zonen")
        led_ring_controller.clear()
        vib.value(0)
        return True
    else:
        print("Ude af zonen")
        #THREAD THIS
        #t.start_new_thread(led_ring_controller.bounce,(50,0,0,100))
        #led_ring_controller.bounce(50,0,0,100)
        print("after LED call")
        vib.value(1)
        main.send_debug_info("Ude af zonen")
        return False
