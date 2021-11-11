import math

def main():
    pass


meterPerDeg = 0.0000089

def havDist(lat1, lon1, lat2, lon2):
    R = 6371 #Radius of the earth in km
    rLat = deg2rad(lat2-lat1)
    rLon = deg2rad(lon2-lon1)
    a = math.sin(rLat/2) * math.sin(rLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(rLon/2) * math.sin(rLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d

def deg2rad(deg):
    return deg * (math.pi/180)


def makeZone(playerPos,x,y):
    negResult = []
    result = []
    points = [x*meterPerDeg,y*meterPerDeg]
    for (item1, item2) in zip(points,playerPos):
        result.append(item1+item2)
        negResult.append(item2-item1)

    print(result, negResult)
    return [result,negResult]



makeZone([55.6070031852261, 12.552418380351071],4,5)

if __name__ == "__main__":
    main()
    