import unittest
import networkx as nx

from src.graph_to_smiles import GraphToSmiles


class SimpleCases(unittest.TestCase):
    @staticmethod
    def test_methane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        gts = GraphToSmiles(graph)
        assert(gts.get_smiles() == 'C')

    @staticmethod
    def test_ethane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_edge('C-1', 'C-2')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CC')

    @staticmethod
    def test_butane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CCCC')

    @staticmethod
    def test_methyl_propane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'C-4')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CC(C)C')

    @staticmethod
    def test_ethanol():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('OH-3')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'OH-3')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CCO')

    @staticmethod
    def test_propanone():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('O-4')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'O-4')
        graph.add_edge('C-2', 'O-4')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CC(=O)C')

    @staticmethod
    def test_butyric_acid():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('O-5')
        graph.add_node('OH-6')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'O-5')
        graph.add_edge('C-4', 'O-5')
        graph.add_edge('C-4', 'OH-6')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CCCC(=O)O')

    @staticmethod
    def test_triethylamine():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_node('N-7')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'N-7')
        graph.add_edge('N-7', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('N-7', 'C-5')
        graph.add_edge('C-5', 'C-6')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CCN(CC)CC')

    @staticmethod
    def test_isobutyric_acid():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('O-5')
        graph.add_node('OH-6')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'C-4')
        graph.add_edge('C-4', 'O-5')
        graph.add_edge('C-4', 'O-5')
        graph.add_edge('C-4', 'OH-6')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'CC(C)C(=O)O')


class CyclicCases(unittest.TestCase):
    @staticmethod
    def test_cyclohexane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-5', 'C-6')
        graph.add_edge('C-6', 'C-1')
        gts = GraphToSmiles(graph)
        assert(gts.get_smiles() == 'C1CCCCC1')

    @staticmethod
    def test_1_methyl_3_bromo_cyclohexene_1():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_node('C-7')
        graph.add_node('Cl-8')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-5', 'C-6')
        graph.add_edge('C-6', 'C-1')
        graph.add_edge('C-6', 'C-1')
        graph.add_edge('C-6', 'C-7')
        graph.add_edge('C-2', 'Cl-8')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'C1=C(CCCC1Cl)C')

    @staticmethod
    def test_benzene():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-5', 'C-6')
        graph.add_edge('C-6', 'C-1')
        graph.add_edge('C-6', 'C-1')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'C1=CC=CC=C1')

    @staticmethod
    def test_cubane():
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_node('C-7')
        graph.add_node('C-8')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'C-1')
        graph.add_edge('C-5', 'C-6')
        graph.add_edge('C-6', 'C-7')
        graph.add_edge('C-7', 'C-8')
        graph.add_edge('C-8', 'C-5')
        graph.add_edge('C-1', 'C-5')
        graph.add_edge('C-2', 'C-6')
        graph.add_edge('C-3', 'C-7')
        graph.add_edge('C-4', 'C-8')
        gts = GraphToSmiles(graph)
        assert (gts.get_smiles() == 'C13C4C5C1C2C5C4C23')


if __name__ == '__main__':
    unittest.main()
