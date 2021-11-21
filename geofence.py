#import zone_udregner
#import zone_og_player
import picket, ujson, uio

global my_fence
my_fence = picket.Fence()

def zone_setup(nr, lat:float=0, lon:float=0):
    #import main
    #Disse tre linjer skaber 2 af de 4 hjørner, i koordinater, til en zone, putter dem i en Zone Class.
    #Tredje linje udregner de resterende hjørner, og kan derefter bruges af picket
    #newZone = zone_udregner.makeZone([lat,lon],8,2)
    #newZone = zone_og_player.Zone(newZone[0], newZone[1])
    #newZoneBorders = newZone.calculate_borders(newZone.nwBorder, newZone.seBorder)
    #Finder heading fra magnetometer
    #newZone.get_heading()
    
    #åbner zones.json som indeholder vores predefineret zoner, og trækker dataen ud i en liste.
    with uio.open("zones.json", "r") as o:
        position = ujson.load(o)
        zone = position["Zone "+str(nr)]["Position"]
        #Iterere igennem de forskellige punkter i den valgte zone og supplere dem til my_fence.
        for i in zone:
            my_fence.add_point((float(zone[i][0]), float(zone[i][1])))
        print(my_fence.list_points())
    return