__author__ = 'shane.reed'

import random
import pylab


# # def f(x):
# #     # x is an integer
# #     return int(x + random.choice([0.25, 0.5, 0.75]))
# #
# # print f(1.0)
# random.seed(100)
#
# def f():
#     return random.random()
#
# print f()

import random, pylab
xVals = []
yVals = []
wVals = []
for i in range(1000):
    xVals.append(random.random())
    yVals.append(random.random())
    wVals.append(random.random())
xVals = pylab.array(xVals)
yVals = pylab.array(yVals)
wVals = pylab.array(wVals)
xVals = xVals + xVals
zVals = xVals + yVals
tVals = xVals + yVals + wVals

# # Q3-1
# pylab.hist(tVals)
# pylab.show()

# # Q3-2
# pylab.hist(xVals)
# pylab.show()

# # Q3-3
# pylab.plot(xVals, zVals)
# pylab.show()

# # Q3-4
# pylab.plot(xVals, yVals)
# pylab.show()

# # Q3-5
# pylab.plot(xVals, sorted(yVals))
# pylab.show()

# # Q3-6
# pylab.plot(sorted(xVals), yVals)
# pylab.show()

# Q3-7
pylab.plot(sorted(xVals), sorted(yVals))
pylab.show()

