"""SAX parser for OpenStreetMap.org Data

This is a minimal streaming parser for an XML export from OpenStreetMap.org. It
only extracts roads and can export them as a graph.

Helpful links:

* OpenStreetMap.org's XML docs: https://wiki.openstreetmap.org/wiki/Elements
* Python's Simple API for XML (SAX) package: https://docs.python.org/3/library/xml.sax.html

Example usage is in Jayson's algorithm's repo:

  https://github.com/jfalkner/algorithms/shortest_path

"""

from xml.sax import parse
from xml.sax.handler import ContentHandler


class MyContentHandler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.nodes = {}
        self.ways = []
        self._way_id = None
        self._way_name = None
        self._way_highway = None
        self._way_nodes = []

    def startElement(self, name, attrs):
        if name == 'node':
            self.nodes[attrs['id']] = (attrs['lon'], attrs['lat'])

        if name == 'way':
            self._way_id = attrs['id']
            self._way_name = None
            self._way_highway = None
            self._way_nodes = []

        if name == 'nd':
            self._way_nodes.append(attrs['ref'])

        if name == 'tag':
            if attrs['k'] == 'name':
                self._way_name = attrs['v']
            if attrs['k'] == 'highway':
                self._way_highway = attrs['v']

    def endElement(self, name):
        if name == 'way' and self._way_highway:
            self.ways.append((self._way_id, self._way_name, self._way_nodes))


def graph_from_openstreetmap(xml):
    """Converts OpenStreetMap XML exports to a map of vertices and edges

    Useful to convert open street map data in to something that is easily
    worked with in code examples. e.g. demonstrating Dijkstra's shortest path.

    :param xml: XML export from OpenStreetMap
    :return: graph with street corners as keys (nodes) and a list of roads as values (edges)
    """
    from math import sqrt, pow
    from collections import defaultdict

    # extract roads from the XML
    handler = MyContentHandler()
    parse(xml, handler)

    # only consider named roads
    named_ways = [w for w in handler.ways if w[1]]

    # map all streets to nodes
    node_map = defaultdict(set)
    for _id, name, nodes in named_ways:
        for id in nodes:
            node_map[id].add(name)

    def key(_r1, _r2):
        return (_r1, _r2) if _r1 < _r2 else (_r2, _r1)

    def distance(x1, y1, x2, y2):
        return sqrt(pow((float(x1) - float(x2)), 2) + pow((float(y1) - float(y2)), 2))

    # map all connected roads
    connected_roads = {}
    for _id, r1, nodes in named_ways:
        for node_id in nodes:
            for r2 in node_map[node_id]:
                if r1 != r2:
                    connected_roads[key(r1, r2)] = handler.nodes[node_id]

    # create a fast lookup of all connected roads given a road name
    road2roads = defaultdict(set)
    for r1, r2 in connected_roads.keys():
        road2roads[r1].add(r2)
        road2roads[r2].add(r1)

    # make a graph with street corners as vertices and roads as edges
    graph = defaultdict(list)
    for r1, r2 in connected_roads.keys():
        for r3 in road2roads[r1]:
            if r2 == r3:
                continue
            x1, y1 = connected_roads[key(r1, r2)]
            x2, y2 = connected_roads[key(r1, r3)]
            dist = distance(x1, y1, x2, y2)
            graph[key(r1, r2)].append((key(r1, r3), dist))
        for r3 in road2roads[r2]:
            if r1 == r3:
                continue
            x1, y1 = connected_roads[key(r1, r2)]
            x2, y2 = connected_roads[key(r2, r3)]
            dist = distance(x1, y1, x2, y2)
            graph[key(r1, r2)].append((key(r2, r3), dist))
    return graph
