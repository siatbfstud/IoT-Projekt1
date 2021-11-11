import picket
import GPSfunk

def testzone(lat, lon):
    my_fence = picket.Fence()


    #Inde i zone
    my_fence.add_point((55.706677, 12.538627))
    my_fence.add_point((55.706165, 12.538455))
    my_fence.add_point((55.705993, 12.540409))
    my_fence.add_point((55.706570, 12.540522))
    
    #Ude af zone
#     my_fence.add_point((55.707020, 12.537976))
#     my_fence.add_point((55.707026, 12.537022))
#     my_fence.add_point((55.707507, 12.537038))
#     my_fence.add_point((55.707581, 12.538344))

#     assert my_fence.check_point((lat, lon)), "The statement is false :D"
    if my_fence.check_point((lat, lon)) == True:
        print("Inde i zonen")
    else:
        print("Ude af zonen")