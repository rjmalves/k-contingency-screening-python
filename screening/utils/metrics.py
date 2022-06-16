from typing import Dict, Tuple
import networkx as nx


def centrality(g: nx.Graph) -> Dict[str, float]:
    return nx.current_flow_betweenness_centrality(g)


def edge_clustering_coefficient(G: nx.Graph
                                ) -> Dict[Tuple[str, str],
                                          float]:
    pass
