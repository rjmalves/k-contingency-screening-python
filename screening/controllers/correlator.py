from typing import List, Dict, Callable
import networkx as nx
import pandas as pd

from screening.models.network import Network
from screening.controllers.screener import Screener


class Correlator:

    def __init__(self,
                 network: Network,
                 screener: Screener):
        self.__network = network
        self.__screener = screener
        self.__metrics = None

    @staticmethod
    def __node_pair_metrics() -> Dict[str, Callable]:
        return

    @staticmethod
    def __edge_metrics() -> Dict[str, Callable]:
        return {
            "EdgeBetweenness": nx.edge_betweenness_centrality,
            "EdgeCFB": nx.edge_current_flow_betweenness_centrality,
            "EdgeLoadCentrality": nx.edge_load_centrality
            }

    def __eval_node_pair_metrics(self) -> pd.DataFrame:
        return pd.DataFrame()

    def __eval_edge_metrics(self) -> pd.DataFrame:
        metrics = Correlator.__edge_metrics()
        G = self.__network.graph
        indices = []
        results = {e: [] for e in G.edges}
        for n, m in metrics.items():
            indices.append(n)
            metric_value = m(G)
            for e in G.edges:
                if e not in metric_value:
                    e_m = (e[1], e[0])
                else:
                    e_m = e
                results[e].append(metric_value[e_m])
        # Adds the metrics from the screener
        for k in range(1, 5):
            indices.append(f"DeltaCFBk{k}")
            metric_value = self.__screener.normalized_global_deltas(k)
            for e in G.edges:
                results[e].append(metric_value[e])
        # Makes the DF for viewing the results
        df_result = pd.DataFrame(data=results,
                                 index=indices)
        return df_result.T

    def __eval_metrics(self) -> List[Callable]:
        return pd.concat([self.__eval_node_pair_metrics(),
                          self.__eval_edge_metrics()])

    @property
    def metrics(self) -> pd.DataFrame:
        if self.__metrics is None:
            self.__metrics = self.__eval_metrics()
        return self.__metrics

    # TODO - Calcular métricas básicas de arestas
    # Calcular métricas para os pares de nós que envolvem a aresta
    # Montar um DF com todos os valores
    # Analisar correlações com seaborn pairplot
