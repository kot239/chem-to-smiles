import networkx as nx


class LinesToGraph:
    def __init__(self, lines, groups):
        self._lines = lines
        self._groups = groups
        self._graph = nx.MultiGraph()
        self._node_id = 0
        self._node_pos = {}

    @staticmethod
    def in_rect(dot, rect):
        return (rect[0][0] <= dot[0] <= rect[1][0]) and (rect[0][1] <= dot[1] <= rect[1][1])

    @staticmethod
    def close_dotes(fst, snd, threshold=25):
        return (fst[0] - snd[0]) ** 2 + (fst[1] - snd[1]) ** 2 <= threshold

    def make_node(self, group_name, tl, br, indent):
        self._node_id += 1
        node_name = group_name + '-' + str(self._node_id)
        self._graph.add_node(node_name)
        self._node_pos[node_name] = ((max(0, tl[0] - indent), max(0, tl[1] - indent)),
                                     (min(512, br[0] + indent), min(512, br[1] + indent)))

    def make_nodes_from_group(self, delta=10):
        for group in self._groups:
            self.make_node(group[1], group[0][0], group[0][1], delta)

    def make_nodes_from_intersections(self, threshold=25, bound=30):
        for i, line in enumerate(self._lines):
            ends = [(line[0], line[1]), (line[2], line[3])]
            connected = [False, False]
            for key, value in self._node_pos.items():
                for k in range(2):
                    connected[k] |= self.in_rect(ends[k], value)

            for k in range(2):
                if not connected[k]:
                    done = False
                    for j in range(i + 1, len(self._lines)):
                        if (self.close_dotes(ends[k], (self._lines[j][0], self._lines[j][1]), threshold) or
                                self.close_dotes(ends[k], (self._lines[j][2], self._lines[j][3]), threshold)):
                            self.make_node('C', ends[k], ends[k], bound)
                            done = True
                            break
                    if not done:
                        self.make_node('C', ends[k], ends[k], bound)

    def connect_nodes(self):
        for line in self._lines:
            ends = [(line[0], line[1]), (line[2], line[3])]
            nodes = [None, None]
            for k in range(2):
                for key, value in self._node_pos.items():
                    if self.in_rect(ends[k], value):
                        nodes[k] = key
                        break
            if (nodes[0] is not None) and (nodes[1] is not None):
                self._graph.add_edge(nodes[0], nodes[1])

    def make_graph(self):
        self.make_nodes_from_group()
        self.make_nodes_from_intersections()
        self.connect_nodes()
        return self._graph
