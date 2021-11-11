import picket
import gpsfunk
import haversine
import PlayerClass


my_fence = picket.Fence()

def zone_setup(lat,lon):
    mkzoneRes = haversine.makeZone([lat,lon],1,1)
    testZone = PlayerClass.Zone(mkzoneRes[0], mkzoneRes[1])
    borders = testZone.calculate_borders(testZone.nwBorder, testZone.seBorder)
    for i in range(4):
        my_fence.add_point(borders[i])
    print(my_fence.points)

def testzone(lat, lon):
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

#     assert my_fence.check_point((lat, lon)), "The statement is false :D"
    if my_fence.check_point((lat, lon)) == True:
        print("Inde i zonen")
        return True
    else:
        print("Ude af zonen")
        return False