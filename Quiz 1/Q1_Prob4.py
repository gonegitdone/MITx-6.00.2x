import pylab

class Location(object):
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)

    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


import random
import math

class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name


# NEW CODE
# The following function is new, and returns the actual x and y distance from the start point to the end point of a
# random walk.

def walkVector(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())


# DRUNK VARIATIONS
# Here are several different variations on a drunk.

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,1.0), (0.0,-1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,0.9), (0.0,-1.03), (1.03, 0.0), (-1.03, 0.0)]
        return random.choice(stepChoices)

class EDrunk(Drunk):
    def takeStep(self):
        ang = 2 * math.pi * random.random()
        length = 0.5 + 0.5 * random.random()
        return (length * math.sin(ang), length * math.cos(ang))

class PhotoDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.0, 0.5),(0.0, -0.5),
                     (1.5, 0.0),(-1.5, 0.0)]
        return random.choice(stepChoices)

class DDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.85, 0.85), (-0.85, -0.85),
                     (-0.56, 0.56), (0.56, -0.56)]
        return random.choice(stepChoices)

# drunks = {}
# # drunk = UsualDrunk('usualDrunk')
# # drunk = ColdDrunk('coldDrunk')
# drunk = EDrunk('EDrunk')
# # pylab.ylim([-100,100])
# # pylab.xlim([-100,100])
# field = Field()
# start = Location(0.0,0.0)
# field.addDrunk(drunk, start)
#
# walkList = []
# for i in range(2):
#     x = walkVector(field,drunk, 100)
#     print x
#     walkList.append(x)

# pylab.plot(walkList, 'ro')
# pylab.show()



def test():
    x = [(1.2537712550937505, 0.8555454111332903), (1.0653990193120522, -4.040633193020806)]
    print x[0][1]

# print test()

def simWalks(numSteps, numTrials, dClass):
    homer = dClass('Homer')
    origin = Location(0, 0)
    position = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(homer, origin)
        position.append(walkVector(f, homer, numSteps))
    x_axis = [p[0] for p in position]
    y_axis = [p[1] for p in position]
    pylab.scatter(x_axis, y_axis)
    pylab.title(dClass.__name__ + 'position')
    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.ylim([-100,100])
    pylab.xlim([-100,100])
    pylab.xlabel('x axis')
    pylab.ylabel('y axis')
    pylab.show()


simWalks(1000, 10000, UsualDrunk)
simWalks(1000, 10000, ColdDrunk)
simWalks(1000, 10000, EDrunk)
simWalks(1000, 10000, PhotoDrunk)
simWalks(1000, 10000, DDrunk)
