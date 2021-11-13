from typing import Dict, Tuple
import matplotlib
import numpy as np
import networkx as nx
from networkx.readwrite import read_edgelist
from networkx.algorithms.centrality import current_flow_betweenness_centrality


g: nx.Graph = read_edgelist("graphs/itaipu11.txt")

def cfb_deltas(g: nx.Graph) -> Dict[Tuple[str, str], float]:

    def __eval_deltas(cfb_ref: Dict[str, float],
                      cfb_removal: Dict[str, float]
                      ) -> float:
        deltas: Dict[str, float] = {}
        for k, v in cfb_ref.items():
            deltas[k] = abs(cfb_removal[k] - v)
        return sum(list(deltas.values()))

    cfb_ref = current_flow_betweenness_centrality(g)
    result: Dict[Tuple[str, str], float] = {}
    edges = list(g.edges)
    for e in edges:
        g.remove_edge(*e)
        if not nx.is_connected(g):
            result[e] = np.inf
        else:
            cfb_removal = current_flow_betweenness_centrality(g)
            result[e] = __eval_deltas(cfb_ref, cfb_removal)
        g.add_edge(*e)

    return result

cfb_deltas(g)

from screening.models.network import Network
from screening.controllers.screener import Screener
from screening.controllers.viewer import Viewer
import matplotlib.pyplot as plt
n = Network.from_edgelist("graphs/itaipu11.txt")
s = Screener(n)
v = Viewer(n, s)
fig = v.global_deltas_graph_plot(4)
plt.savefig("t11_k4.png")
