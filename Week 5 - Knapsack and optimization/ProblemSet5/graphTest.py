from graph import *


# ====================Test Area======================================================
g = WeightedDigraph()
na = Node('a')
nb = Node('b')
nc = Node('c')
g.addNode(na)
g.addNode(nb)
g.addNode(nc)
e1 = WeightedEdge(na, nb, 15, 10)
print e1
# a->b (15, 10)
print e1.getTotalDistance()
# 15
print e1.getOutdoorDistance()
# 10
e2 = WeightedEdge(na, nc, 14, 6)
e3 = WeightedEdge(nb, nc, 3, 1)
print e2
# a->c (14, 6)
print e3
# b->c (3, 1)
g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
print '*********'
print g
# a->b (15.0, 10.0)
# a->c (14.0, 6.0)
# b->c (3.0, 1.0)
print g.childrenOf(na)
print '***'
print e2.getSource()
print e2.getDestination()
print g.childrenOf(na)
print g.childrenOf(nb)
print g.childrenOf(nc)

print '================test 8========================'
print 'results should be \n','y-> z, (20.0, 1.0) \n','x-> y, (18.0, 8.0) \n','z-> x, (7.0, 6.0)\n', '****'
nx = Node('x')
ny = Node('y')
nz = Node('z')
e1 = WeightedEdge(nx, ny, 18, 8)
e2 = WeightedEdge(ny, nz, 20, 1)
e3 = WeightedEdge(nz, nx, 7, 6)
g = WeightedDigraph()
g.addNode(nx)
g.addNode(ny)
g.addNode(nz)
g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
print g
print '================test 9========================'
print 'results should be \n','k-> m, (100.0, 65.0)\n','k-> g, (84.0, 5.0)\n','j-> k, (55.0, 30.0)\n', 'm-> k, (74.0, 5.0)\n', 'm-> k, (24.0, 20.0)\n', 'g-> m, (29.0, 19.0)\n', 'g-> m, (62.0, 31.0)\n', 'g-> k, (19.0, 19.0)\n', '****'
nj = Node('j')
nk = Node('k')
nm = Node('m')
ng = Node('g')
g = WeightedDigraph()
g.addNode(nj)
g.addNode(nk)
g.addNode(nm)
g.addNode(ng)
randomEdge = WeightedEdge(nm, nk, 74, 5)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nj, nk, 55, 30)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(ng, nm, 29, 19)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nk, nm, 100, 65)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(ng, nm, 62, 31)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nk, ng, 84, 5)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(ng, nk, 19, 19)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nk, 24, 20)
g.addEdge(randomEdge)
print g