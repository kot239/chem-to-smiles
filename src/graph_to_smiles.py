class GraphToSmiles:
    def __init__(self, graph):
        self._graph = graph
        self._was = {node: False for node in graph.nodes}
        self._breaks = {node: [] for node in graph.nodes}
        self._deleted_edges = set()
        self._break = 0
        self._tree = {node: [] for node in graph.nodes}
        self._root = None

    def add_break(self, nodes):
        self._break += 1
        self._deleted_edges.add(nodes)
        self._deleted_edges.add((nodes[1], nodes[0]))
        for node in nodes:
            self._breaks[node].append(str(self._break))

    def dfs(self, node, prev):
        self._was[node] = True
        neighs = [v for v in self._graph.neighbors(node)]
        if prev is not None:
            neighs.remove(prev)
        neighs = sorted(neighs, key=lambda v: len(self._graph.get_edge_data(node, v)), reverse=True)
        for i, child in enumerate(neighs):
            if len(self._graph.get_edge_data(node, child)) == 2:
                adj = '='
            elif len(self._graph.get_edge_data(node, child)) == 3:
                adj = '#'
            else:
                adj = ''
            if self._was[child]:
                if (node, child) not in self._deleted_edges:
                    self.add_break((node, child))
            else:
                self._tree[node].append((adj, child))
                self.dfs(child, node)

    def build_smiles(self, node):
        accum = ''
        left = '('
        right = ')'
        for i, u in enumerate(self._tree[node]):
            if i + 1 == len(self._tree[node]):
                left = ''
                right = ''
            accum += left + u[0] + self.build_smiles(u[1]) + right
        return node[:node.find('-')] + ''.join(self._breaks[node]) + accum

    def get_smiles(self):
        for node in self._graph.nodes:
            if node[:node.find('-')] == 'C':
                self._root = node
                break
        self.dfs(self._root, None)
        return self.build_smiles(self._root)
