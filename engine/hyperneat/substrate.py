import math

class Substrate:

    def __init__(self):

        self.nodes = {}

        self.nodes = {
            "dosR":  (-1.0,  1.0),
            "sigH":  ( 1.0,  1.0),
            "sigE":  (-1.0,  0.0),
            "whiB3": ( 1.0,  0.0),
            "phoP":  (-1.0, -1.0),
            "mprA":  ( 1.0, -1.0)
        }

    def position(self, node):

        return self.nodes[node]
    
    def node_names(self):

        return list(self.nodes.keys())
    
    def all_connections(self):

        pairs = []

        names = self.node_names()

        for source in names:

            for target in names:

                if source != target:

                    pairs.append((source, target))

        return pairs

    def distance(self, a, b):

        x1, y1 = self.position(a)

        x2, y2 = self.position(b)

        return math.sqrt(

            (x2 - x1) ** 2 +

            (y2 - y1) ** 2
        )

    def cppn_inputs(self, source, target):

        x1, y1 = self.position(source)

        x2, y2 = self.position(target)

        d = self.distance(source, target)

        return [x1, y1, x2, y2, d, 1.0]