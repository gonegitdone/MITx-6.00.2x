__author__ = 'shane.reed'

# L5 PROBLEM 1  (5 points possible)
# You have a bucket with 3 red balls and 3 green balls. Assume that once you draw a ball out of the bucket,
# you don't replace it. What is the probability of drawing 3 balls of the same color?
#
# Write a Monte Carlo simulation to solve the above problem. Feel free to write a helper function if you wish.

import random
def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3
    balls of the same color were drawn.
    '''

    def drawBalls():
        draw = []
        bucket = ['R', 'R', 'R', 'G', 'G', 'G']
        for i in range(3):
            pick = random.randrange(0,len(bucket) - 1)
            draw.append(bucket.pop(pick))
        if draw == ['R', 'R', 'R'] or draw == ['G', 'G', 'G']:
            return 1
        else:
            return 0

    sameColour = 0
    for i in range(numTrials):
        sameColour += drawBalls()
    return float(sameColour)/numTrials

print noReplacementSimulation(5000)