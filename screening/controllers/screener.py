from typing import Dict, Tuple
import networkx as nx
import numpy as np
from networkx.algorithms.centrality import current_flow_betweenness_centrality

from screening.models.network import Network


class Screener:
    def __init__(self,
                 network: Network):
        self.__network = network
        self.__reference_centrality = None
        self.__deltas: Dict[int,
                            Dict[tuple,
                                 float]] = {}
        self.__global_deltas: Dict[int,
                                   Dict[tuple,
                                        float]] = {}

    def __eval_delta_contingency(self,
                                 contingency: tuple
                                 ) -> float:
        deltas: Dict[str, float] = {}
        self.network.graph.remove_edges_from(contingency)
        removal_centrality = self.__centrality(self.network.graph)
        self.network.graph.add_edges_from(contingency)
        for k, v in self.reference_centrality.items():
            deltas[k] = abs(removal_centrality[k] - v)
        return sum(list(deltas.values()))

    def __eval_deltas(self, order: int):
        deltas: Dict[tuple, float] = {}
        for c in self.network.valid_contingencies(order):
            deltas[tuple(c)] = self.__eval_delta_contingency(c)
        self.__deltas[order] = deltas

    def deltas(self, order: int) -> Dict[tuple, float]:
        if order not in self.__deltas:
            self.__eval_deltas(order)
        return self.__deltas[order]

    def __eval_global_deltas(self, order: int):
        deltas = self.deltas(order)
        edges = list(self.__network.graph.edges)
        global_deltas = {e: 0 for e in edges}
        for contingency, delta in deltas.items():
            for edge in contingency:
                global_deltas[edge] += delta
        self.__global_deltas[order] = global_deltas

    def global_deltas(self, order: int) -> Dict[Tuple[str, str],
                                                float]:
        if order not in self.__global_deltas:
            self.__eval_global_deltas(order)
        return self.__global_deltas[order]

    def normalized_global_deltas(self, order) -> Dict[Tuple[str, str],
                                                      float]:
        deltas = self.global_deltas(order)
        max = np.max(list(deltas.values()))
        norm_deltas = {e: d / max for e, d in deltas.items()}
        return norm_deltas

    def __centrality(self, g: nx.Graph) -> Dict[str, float]:
        return current_flow_betweenness_centrality(g)

    @property
    def network(self) -> Network:
        return self.__network

    @property
    def reference_centrality(self) -> Dict[str, float]:
        if self.__reference_centrality is None:
            self.__reference_centrality = self.__centrality(self.network.graph)
        return self.__reference_centrality
