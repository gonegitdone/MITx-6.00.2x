import random, pylab

# You are given this function
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    # TODO
    pylab.hist(values, numBins)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    if title != None:
        pylab.title(title)
    pylab.show()

# print makeHistogram([1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,5,5,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-3,-3,-3,-3,-4,-4,-5,-5], 10, 'xLabel', 'yLabel', 'myTitle')
# print makeHistogram([1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,5,5,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-3,-3,-3,-3,-4,-4,-5,-5], 10, 'xLabel', 'yLabel')

# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    # TODO
    meanList = []
    for trial in range(numTrials):
        longestRun = 0
        lastRoll = 0
        thisStreak = 1
        for roll in range(numRolls):
            thisRoll = die.roll()
            # print thisRoll
            if thisRoll == lastRoll:
                thisStreak += 1
            else:
                thisStreak = 1
            if thisStreak > longestRun:
                longestRun = thisStreak
            lastRoll = thisRoll
        meanList.append(longestRun)
    # print meanList
    makeHistogram(meanList, 10, 'Longest Run', 'Run Total', 'Longest Consecutive Rolls')
    mean, dev = getMeanAndStd(meanList)
    return mean



# random.seed(0)
# One test case
print 'Example test case: ', getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000), '   Answer should be 5.312'
# print getAverage(Die([1,2,3,4,5,6,6,6,7]), 100, 10)
print 'Test 1: ', getAverage(Die([1]), 10, 1000)
print 'Test 2: ', getAverage(Die([1,1]), 10, 1000)
print 'Test 3: ', getAverage(Die([1,2,3,4,5,6]), 50, 1000)
print 'Test 4: ', getAverage(Die([1,2,3,4,5,6,6,6,7]), 50, 1000)
print 'Test 5: ', getAverage(Die([1,2,3,4,5,6,6,6,7]), 1, 1000)