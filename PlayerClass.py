#import haversine
#import math

class Zone:
    """Class for hver enkelte zone"""

    def __init__(self, nwBorder:tuple, seBorder:tuple):
        self.nwBorder = nwBorder
        self.seBorder = seBorder
        self.borders = [nwBorder,seBorder]

    #Udregner zonens 4 hjørner, ved hjælp af 2 modsatte hjørner.
    def calculate_borders(self, nwBorder:list, seBorder:list):
        borders = [nwBorder,
                    [seBorder[0],nwBorder[1]],
                    seBorder,
                    [nwBorder[0],seBorder[1]]]
        self.borders = borders
        #print(borders)
        return borders
    
    """ def rotate_zone(self, origin, points, angle):
        
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in degrees.
       
        angle = math.radians(angle)
        ox, oy = origin
        
        #px, py = points
        newPoints = []
        for i in points:
            qx = ox + math.cos(angle) * (i[0] - ox) - math.sin(angle) * (i[1] - oy)
            qy = oy + math.sin(angle) * (i[0] - ox) + math.cos(angle) * (i[1] - oy)
            newPoints.append([qx,qy])

        return newPoints """  
    


class Player:
    """Class for hver spiller/GPS enhed"""
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.pos = [lat,lon]


#zone1 = Zone([1,9], (7,3))
#player1 = Player(55.64266121248321, 12.612958544710214)

#nextBorderCal = haversine.makeZone(player1.pos,5,10)

#Længde og breddegrader for zone
#Zone.calculate_borders(Zone, nextBorderCal[0],nextBorderCal[1])




