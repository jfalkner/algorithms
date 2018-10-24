"""Shortest path example

Example from Wikipedia: https://en.wikipedia.org/wiki/Shortest_path_problem
"""
from dijkstra import shortest_paths, print_path


# make up an example graph
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('E', 3)],
    'D': [('F', 11)],
    'E': [('D', 4)],
    'F': [],
}

# find all paths from your starting location
paths = shortest_paths(graph, 'A')
print_path(paths, 'A', 'F')
