import unittest
import networkx as nx

from src.graph_to_smiles import GraphToSmiles


class SimpleCases(unittest.TestCase):
    def test_methane(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'C')

    def test_ethane(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_edge('C-1', 'C-2')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'CC')

    def test_butane(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'CCCC')

    def test_methyl_propane(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'C-4')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'CC(C)C')

    def test_ethanol(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('OH-3')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'OH-3')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'CCO')

    def test_propanone(self):
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
        self.assertEqual(gts.get_smiles(), 'CC(=O)C')

    def test_butyric_acid(self):
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
        self.assertEqual(gts.get_smiles(), 'CCCC(=O)O')

    def test_triethylamine(self):
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
        self.assertEqual(gts.get_smiles(), 'CCN(CC)CC')

    def test_isobutyric_acid(self):
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
        self.assertEqual(gts.get_smiles(), 'CC(C)C(=O)O')


class CyclicCases(unittest.TestCase):
    def test_cyclohexane(self):
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
        self.assertEqual(gts.get_smiles(), 'C1CCCCC1')

    def test_1_methyl_3_bromo_cyclohexene_1(self):
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
        self.assertEqual(gts.get_smiles(), 'C1=C(CCCC1Cl)C')

    def test_benzene(self):
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
        self.assertEqual(gts.get_smiles(), 'C1=CC=CC=C1')

    def test_cubane(self):
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
        self.assertEqual(gts.get_smiles(), 'C13C4C5C1C2C5C4C23')

    def test_butanediamine(self):
        graph = nx.MultiGraph()
        graph.add_node('C-1')
        graph.add_node('C-2')
        graph.add_node('C-3')
        graph.add_node('C-4')
        graph.add_node('C-5')
        graph.add_node('C-6')
        graph.add_node('C-7')
        graph.add_node('C-8')
        graph.add_node('C-9')
        graph.add_node('C-10')
        graph.add_node('C-11')
        graph.add_node('C-12')
        graph.add_node('C-13')
        graph.add_node('C-14')
        graph.add_node('C-15')
        graph.add_node('C-16')
        graph.add_node('N-17')
        graph.add_node('N-18')
        graph.add_node('N-19')
        graph.add_node('N-20')
        graph.add_edge('C-1', 'N-17')
        graph.add_edge('C-1', 'N-17')
        graph.add_edge('C-1', 'C-2')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-2', 'C-3')
        graph.add_edge('C-3', 'C-4')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-4', 'C-5')
        graph.add_edge('C-5', 'N-17')
        graph.add_edge('C-5', 'C-6')
        graph.add_edge('C-6', 'N-18')
        graph.add_edge('C-6', 'N-18')
        graph.add_edge('C-7', 'N-18')
        graph.add_edge('C-7', 'C-8')
        graph.add_edge('C-9', 'N-19')
        graph.add_edge('C-9', 'C-10')
        graph.add_edge('C-9', 'C-10')
        graph.add_edge('C-10', 'C-11')
        graph.add_edge('C-11', 'C-12')
        graph.add_edge('C-11', 'C-12')
        graph.add_edge('C-12', 'C-13')
        graph.add_edge('C-13', 'N-19')
        graph.add_edge('C-13', 'N-19')
        graph.add_edge('C-13', 'C-14')
        graph.add_edge('C-14', 'N-20')
        graph.add_edge('C-14', 'N-20')
        graph.add_edge('C-15', 'N-20')
        graph.add_edge('C-15', 'C-16')
        graph.add_edge('C-8', 'C-16')
        gts = GraphToSmiles(graph)
        self.assertEqual(gts.get_smiles(), 'C1=NC(=CC=C1)C=NCCCCN=CC2=NC=CC=C2')


if __name__ == '__main__':
    unittest.main()
