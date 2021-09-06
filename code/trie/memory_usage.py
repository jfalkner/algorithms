"""
Comparison of memory used by different Python data structures for a trire-based DNA
analysis algorithm
"""
from collections import namedtuple

from pympler.asizeof import asized


class Node:
    def __init__(self, A=None, C=None, G=None, T=None, N=None):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N

# use datamodel to avoid object dict creation: https://docs.python.org/3/reference/datamodel.html#slots
class NodeSlots:
    __slots__ = 'A', 'C', 'T', 'G', 'N', 'count'
    def __init__(self, A=None, C=None, G=None, T=None, N=None):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N
        self.count = 0

class NodeSlotsNoCount:
    __slots__ = 'A', 'C', 'T', 'G', 'N'
    def __init__(self, A=None, C=None, G=None, T=None, N=None):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N


# dict use will have a key for each alphabet character and one for count
example_dict = {'A': None, 'C': None, 'G': None, 'T': None, 'N': None, 'count': 0}

node_tuple = namedtuple('NodeTuple', 'A C G T N count')
example_namedtuple = node_tuple(None, None, None, None, None, 0)

# Each tuple will have 5 children tuples (or None vals) and a count
example_tuple = (None, None, None, None, None, 0)


class NodeCompressed:
    __slots__ = 'sequence', 'next'
    def __init__(self, sequence, next_node):
        self.sequence = sequence
        self.next = next_node

print(f"""
Memory Usage Per Datastructure

* Class = {asized(Node()).size}
* Class w/__slots__ = {asized(NodeSlots()).size}
* Class w/__slots__ No Count= {asized(NodeSlotsNoCount()).size}
* Dict = {asized(example_dict).size}
* namedtuple = {asized(example_namedtuple).size}
* Tuple = {asized(example_tuple).size}

Bonus
* NodeCompressed = {asized(NodeCompressed('CGGCGG', None)).size}
* int = {asized(1).size}
""")
