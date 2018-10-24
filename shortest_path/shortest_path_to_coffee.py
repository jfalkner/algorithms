"""Shortest paths in Ann Arbor, MI

A practical example of applying shortest path algorithms to real data. In this
case, finding the best way to walk to local coffee shops in Ann Arbor, MI.

OpenStreetMap of Ann Arbor, MI
https://www.openstreetmap.org/export#map=15/42.2758/-83.7501
"""
import gzip
from xml.sax import parse
from xml.sax.handler import ContentHandler

from openstreetmap import graph_from_openstreetmap
from dijkstra import shortest_paths, print_path


# load Ann Arbor as a graph
graph = graph_from_openstreetmap(gzip.open('openstreetmap_ann_arbor_mi.xml.gz'))

# find all paths from your starting location
start = ('Crest Avenue', 'West Washington Street')
paths = shortest_paths(graph, start)

# Confirm it is right for known spots -- nearby coffee shops
# Argus
print("\nArgus @ ('Second Street', 'West Liberty Street')")
print_path(paths, start, (u'Second Street', u'West Liberty Street'))

# Big City Small World Bakery
print("\nBig City Small World Bakery @ ('Miller Avenue', 'Spring Street')")
print_path(paths, start, (u'Miller Avenue', u'Spring Street'))

# Jefferson Cakery
print("\nJefferson Cakery @ ('Fifth Street', 'West Jefferson Street')")
print_path(paths, start, (u'Fifth Street', u'West Jefferson Street'))
