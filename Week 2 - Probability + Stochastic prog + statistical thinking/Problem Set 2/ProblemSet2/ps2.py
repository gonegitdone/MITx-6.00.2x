# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanedTiles = []
        # self.pos = Position(self.width/2,self.height/2)
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # pos = Position()
        self.pos = pos
        self.x = math.floor(self.pos.getX())
        self.y = math.floor(self.pos.getY())
        if (self.x, self.y) not in self.cleanedTiles:
            self.cleanedTiles.append((self.x, self.y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m, n) in self.cleanedTiles:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanedTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        newX = random.random() * self.width
        newY = random.random() * self.height
        return Position(newX, newY)


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        self.pos = pos
        x = math.floor(self.pos.getX())
        y = math.floor(self.pos.getY())
        if 0 <= x <= (self.width - 1) and 0 <= y <= (self.height - 1):
            return True
        else:
            return False

# random.seed(0)
# room = RectangularRoom(3,2)
# print 'Room width: ', room.width
# print 'Room Height: ', room.height
# print 'Number of tiles in room: ', room.getNumTiles()
# print  'Get number of tiles cleaned: ', room.getNumCleanedTiles()
# print 'Clean tile at position 0.6, 1', room.cleanTileAtPosition(Position(0.6,1))
# print  'Get number of tiles cleaned (should have increased) : ', room.getNumCleanedTiles()
# print 'Clean tile at position 0.6, 1', room.cleanTileAtPosition(Position(0.6,1))
# print  'Get number of tiles cleaned (should NOT have increased) : ', room.getNumCleanedTiles()
# print room.getRandomPosition()
# pos = room.getRandomPosition()
# print 'Is position in room (should be false): ', room.isPositionInRoom(pos)
# print 'Is position in room (should be false): ', room.isPositionInRoom(Position(-5.76, 5.13))
# print 'Is position in room (should be true): ', room.isPositionInRoom(Position(0.6,1))
# print 'cleaned tiles list: ', room.cleanedTiles
# print 'Is tile cleaned (should be true): ', room.isTileCleaned(0.0, 1.0)
# print 'Is tile cleaned (should be false): ', room.isTileCleaned(3.0, 1.0)
# print 'Is tile cleaned (should be false): ', room.isTileCleaned(pos.getX(), pos.getY())

# def randPosMult(numberTries = 100):
#     room = RectangularRoom(10,10)
#     for i in range(numberTries):
#         pos = room.getRandomPosition()
#         print 'iteration #', str(i),'  Random position : ', pos, 'Position in room ? ', room.isPositionInRoom(pos)
#
# randPosMult(100)

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.POSITION = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.POSITION)
        self.DIRECTION = random.random() * 359


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.POSITION
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.DIRECTION

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.POSITION = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if 0 <= direction < 360:
            self.DIRECTION = direction
        elif direction >= 360:
            self.DIRECTION = 359
        else:
            self.DIRECTION = 0

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

'''# speed = 0.5
# room = RectangularRoom(10,10)
# myRobot = Robot(room,0.5)
# print 'get robot initial position: ', myRobot.getRobotPosition()
# print 'get robot initial direction: ', myRobot.getRobotDirection()
# print 'get number of room cleaned tiles', room.getNumCleanedTiles()
# myRobot.setRobotPosition(Position(1.0,1.0))
# print 'set robot position to (1,1) \nRobot position:   ', myRobot.getRobotPosition()
# myRobot.setRobotDirection(400)
# print 'set robot direction to 400 \nRobot position should equal 360 (clamped):   ', myRobot.getRobotDirection()
# myRobot.setRobotDirection(-400)
# print 'set robot direction to -400 \nRobot position should equal 0 (clamped):   ', myRobot.getRobotDirection()
# myRobot.setRobotDirection(148)
# print 'set robot direction to 148 \nRobot position should equal 148:   ', myRobot.getRobotDirection()
'''

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        direction = self.getRobotDirection()
        currentPosition = self.getRobotPosition()
        newPosition = currentPosition.getNewPosition(direction, self.speed)
        if self.room.isPositionInRoom(newPosition):
            self.setRobotPosition(newPosition)
            position = self.getRobotPosition()
            self.room.cleanTileAtPosition(position)
        else:
            self.setRobotDirection(random.random() * 359)
            self.updatePositionAndClean()


# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)

# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    def cleanRoom(robots):
        clockTicks = 0
        while room.getNumCleanedTiles() < minCoverage:
            for robot in robots:
                robot.updatePositionAndClean()
            clockTicks += 1
            anim.update(room, robots)
        return clockTicks

    clockTickResults = []

    for trial in range(num_trials):
        anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.01)
        room = RectangularRoom(width, height)
        totalTiles = room.getNumTiles()
        minCoverage = totalTiles * min_coverage
        robots = []
        for robot in range(num_robots):
            robots.append(robot_type(room, speed))

        clockTickResults.append(cleanRoom(robots))
        anim.done()

    totalClockTicks = 0

    for tick in range(len(clockTickResults)):
        totalClockTicks += clockTickResults[tick]
    avgClockTicks = totalClockTicks / len(clockTickResults)
    return float(avgClockTicks)


''' Test cases
# Uncomment this line to see how much your simulation takes on average
# print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)
# print 'One robot takes around 150 clock ticks to completely clean a 5x5 room'
# print  runSimulation(1, 1.0, 5, 5, 1.0, 30, StandardRobot)
# print 'One robot takes around 190 clock ticks to clean 75% of a 10x10 room'
# print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)
# print 'One robot takes around 310 clock ticks to clean 90% of a 10x10 room'
# print  runSimulation(1, 1.0, 10, 10, 0.9, 30, StandardRobot)
# print 'One robot takes around 3322 clock ticks to completely clean a 20x20 room'
# print  runSimulation(1, 1.0, 20, 20, 1.0, 30, StandardRobot)
# print 'Three robots take around 1105 clock ticks to completely clean a 20x20 room'
# print  runSimulation(3, 1.0, 20, 20, 1.0, 30, StandardRobot)
# print '========================================='
#
# print 'One robot takes around 150 clock ticks to completely clean a 5x5 room'
# print  runSimulation(1, 2.0, 5, 5, 1.0, 30, StandardRobot)
# print 'One robot takes around 190 clock ticks to clean 75% of a 10x10 room'
# print  runSimulation(1, 2.0, 10, 10, 0.75, 30, StandardRobot)
# print 'One robot takes around 310 clock ticks to clean 90% of a 10x10 room'
# print  runSimulation(1, 2.0, 10, 10, 0.9, 30, StandardRobot)
# print 'One robot takes around 3322 clock ticks to completely clean a 20x20 room'
# print  runSimulation(1, 2.0, 20, 20, 1.0, 30, StandardRobot)
# print 'Three robots take around 1105 clock ticks to completely clean a 20x20 room'
# print  runSimulation(3, 2.0, 20, 20, 1.0, 30, StandardRobot)
'''

# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotDirection(random.random() * 359)
        direction = self.getRobotDirection()
        currentPosition = self.getRobotPosition()
        newPosition = currentPosition.getNewPosition(direction, self.speed)
        if self.room.isPositionInRoom(newPosition):
            self.setRobotPosition(newPosition)
            position = self.getRobotPosition()
            self.room.cleanTileAtPosition(position)
        else:
            self.updatePositionAndClean()
        # raise NotImplementedError

# testRobotMovement(StandardRobot, RectangularRoom)
# testRobotMovement(RandomWalkRobot, RectangularRoom)
'''
print 'One robot takes around 150 clock ticks to completely clean a 5x5 room'
print  runSimulation(1, 1.0, 5, 5, 1.0, 30, RandomWalkRobot)
print 'One robot takes around 190 clock ticks to clean 75% of a 10x10 room'
print  runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot)
print 'One robot takes around 310 clock ticks to clean 90% of a 10x10 room'
print  runSimulation(1, 1.0, 10, 10, 0.9, 30, RandomWalkRobot)
print 'One robot takes around 3322 clock ticks to completely clean a 20x20 room'
print  runSimulation(1, 1.0, 20, 20, 1.0, 30, RandomWalkRobot)
print 'Three robots take around 1105 clock ticks to completely clean a 20x20 room'
print  runSimulation(3, 1.0, 20, 20, 1.0, 30, RandomWalkRobot)
print '========================================='

print 'One robot takes around 150 clock ticks to completely clean a 5x5 room'
print  runSimulation(1, 2.0, 5, 5, 1.0, 30, RandomWalkRobot)
print 'One robot takes around 190 clock ticks to clean 75% of a 10x10 room'
print  runSimulation(1, 2.0, 10, 10, 0.75, 30, RandomWalkRobot)
print 'One robot takes around 310 clock ticks to clean 90% of a 10x10 room'
print  runSimulation(1, 2.0, 10, 10, 0.9, 30, RandomWalkRobot)
print 'One robot takes around 3322 clock ticks to completely clean a 20x20 room'
print  runSimulation(1, 2.0, 20, 20, 1.0, 30, RandomWalkRobot)
print 'Three robots take around 1105 clock ticks to completely clean a 20x20 room'
print  runSimulation(3, 2.0, 20, 20, 1.0, 30, RandomWalkRobot)
'''

# print  runSimulation(1, 1.0, 5, 5, 1.0, 1, StandardRobot)
# print  runSimulation(1, 1.0, 5, 5, 1.0, 1, RandomWalkRobot)


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)

showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room', 'Number of Robots','Time-Steps')

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
showPlot2('Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms', 'Aspect Ratio', 'Time-Steps')
