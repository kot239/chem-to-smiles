import unittest
import networkx as nx
from src.lines_to_graph import LinesToGraph


class LinesCases(unittest.TestCase):
    def test_ethane(self):
        lines = [[4, 4, 255, 255]]
        groups = []
        ltg = LinesToGraph(lines, groups)
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_edge('C-1', 'C-2')
        self.assertTrue(nx.utils.misc.graphs_equal(ltg.make_graph(), graph))

    def test_ethen(self):
        lines = [[255, 4, 255, 255],
                 [265, 4, 256, 255]]
        groups = []
        ltg = LinesToGraph(lines, groups)
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-1', 'C-2')
        self.assertTrue(nx.utils.misc.graphs_equal(ltg.make_graph(), graph))

    def test_ethanol(self):
        lines = [[120, 106, 100, 256],
                 [100, 256, 120, 406]]
        groups = [[((115, 350), (125, 450)), 'OH']]
        ltg = LinesToGraph(lines, groups)
        graph = nx.MultiGraph()
        graph.add_node('OH-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_edge('OH-1', 'C-3')
        graph.add_edge('C-2', 'C-3')
        self.assertTrue(nx.utils.misc.graphs_equal(ltg.make_graph(), graph))


if __name__ == '__main__':
    unittest.main()
