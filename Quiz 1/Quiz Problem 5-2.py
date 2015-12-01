

import random
def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3
    balls of the same color were drawn in the first 3 draws.
    '''

    def drawBalls():
        draw = []
        bucket = ['R', 'R', 'R', 'R', 'G', 'G', 'G', 'G']
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

print drawing_without_replacement_sim(1000000)