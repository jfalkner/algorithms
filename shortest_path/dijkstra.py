"""Dijkstra's shortest path algorithm

Python example of an O(N log N) style solution to finding the shortest path
from a node to any other node a graph.

These are meant to be simple, white-board style solutions to a commonly
discussed problems.

shortest_paths = Dijkstra's algorithm
  * Time = O((V + E) log V)
    * (V + E) = explores each vertex and edge once
    * log V = timing of heapsort push/pop
  * Memory
    * size of graph -- assume not related but O(V + E)
    * O(V) = map of shortest path to vertex

* print_path = Utility method to show the path. O(N) bound memory use

The graph is in the following example format:

```
# mock example
graph = {
    'a': [('b', 1), ('c', 2)],  # node a connects to b and c, respective distances 1 and 2
    'b': [('d', 1)],
    ...
}

# keys are more complex such as street intersections
graph = {
    ('Main St', '1st St'): [
        (('Main St', '1st St'), 1),
        (('Main St', '2nd St'), 2)],
    ...
}
```
"""
import sys
from heapq import heappush, heappop


def shortest_paths(graph, v_start):
    paths = {}
    queue = [(0, v_start)]
    while queue:
        total_dist, v_dst = heappop(queue)
        for v_nxt, dist in graph[v_dst]:
            _d = total_dist + dist
            if paths.get(v_nxt, (sys.maxsize,))[0] > _d:
                paths[v_nxt] = (_d, v_dst)
                heappush(queue, (_d, v_nxt))
    return paths


def print_path(paths, v_src, v_dst):
    path = [v_dst]
    current = v_dst
    while current != v_src:
        _, _p = paths[current]
        path.append(_p)
        current = _p
    for step in reversed(path):
        print(step)
