__author__ = 'shane.reed'
from ps5 import *

# # Test case map3 B
# map3 = load_map("map3.txt")
# print bruteForceSearch(map3, "1", "3", 18, 18)
# # "['1', '2', '3']"
# print bruteForceSearch(map3, "1", "3", 18, 0)
# # "ValueError successfully raised"
# print bruteForceSearch(map3, "1", "3", 10, 10)
# # "ValueError successfully raised"

map5 = WeightedDigraph()
map5.addNode(Node('1'))
map5.addNode(Node('2'))
map5.addNode(Node('3'))
map5.addNode(Node('4'))
map5.addNode(Node('5'))
map5.addEdge(WeightedEdge(Node('1'), Node('2'), 5, 2))
map5.addEdge(WeightedEdge(Node('3'), Node('5'), 6, 3))
map5.addEdge(WeightedEdge(Node('2'), Node('3'), 20, 10))
map5.addEdge(WeightedEdge(Node('2'), Node('4'), 10, 5))
map5.addEdge(WeightedEdge(Node('4'), Node('3'), 2, 1))
map5.addEdge(WeightedEdge(Node('4'), Node('5'), 20, 10))

print directedDFS(map5, "1", "3", 17, 8)