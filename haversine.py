import math

def main():
    pass

meterPerDeg = 0.0000089

#Skaber en zone ud fra en lokation, f.eks. spilleren. Der måles så i meter fra midten og ud, så zonen passer til hver enkelte spiller.
def makeZone(playerPos,x,y):
    """X og Y er bredde og længde på kassen"""
    negResult = []
    result = []
    
    points = [x*meterPerDeg,y*meterPerDeg]
    for (item1, item2) in zip(points,playerPos):
        result.append(item1+item2)
        negResult.append(item2-item1)

    return [result,negResult]

if __name__ == "__main__":
    main()
    