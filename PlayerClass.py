import haversine

class Zone:
    """Class for hver enkelte zone"""

    def __init__(self, nwBorder:tuple, seBorder:tuple):
        self.nwBorder = nwBorder
        self.seBorder = seBorder
        self.borders = []

    #Udregner zonens 4 hjørner, ved hjælp af 2 modsatte hjørner.
    def calculate_borders(self, nwBorder:list, seBorder:list):
        borders = [nwBorder,
                    [seBorder[0],nwBorder[1]],
                    seBorder,
                    [nwBorder[0],seBorder[1]]]
        self.borders = borders
        print(borders)
        return borders

class Player:
    """Class for hver spiller/GPS enhed"""
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.pos = [lat,lon]


zone1 = Zone([1,9], (7,3))
player1 = Player(55.64266121248321, 12.612958544710214)

nextBorderCal = haversine.makeZone(player1.pos,5,10)

#Længde og breddegrader for zone
Zone.calculate_borders(Zone, nextBorderCal[0],nextBorderCal[1])




