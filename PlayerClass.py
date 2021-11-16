#import haversine
#import math
import hmc5883l

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
    
    def get_heading(self):
        #INDSAMLER MAGNETOMETER DATA OG RETURNER HEADING I GRADER
        sensor = hmc5883l.HMC5883L(scl=22,sda=21)
        x,y,z = sensor.read()
        print(sensor.format_result(x,y,z))
    

    #Skal nok ikke bruges
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







