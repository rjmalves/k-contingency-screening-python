from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from networkx.drawing import draw
from networkx.drawing.layout import spring_layout

from screening.models.network import Network
from screening.controllers.screener import Screener

SEED = 0


class Viewer:

    def __init__(self,
                 network: Network,
                 screener: Screener):
        self.__network = network
        self.__screener = screener

    def global_deltas_bar_plot(self) -> Figure:
        fig, ax = plt.subplots(figsize=(9, 9))
        pass

    def global_deltas_graph_plot(self, order: int) -> Figure:
        fig, ax = plt.subplots(figsize=(9, 9))
        G = self.__network.graph
        deltas = self.__screener.normalized_global_deltas(order)
        colors = list(deltas.values())
        options = {
            "node_color": "#A0CBE2",
            "edge_color": colors,
            "width": 4,
            "edge_cmap": plt.get_cmap("cool"),
            "with_labels": True,
        }
        draw(G, ax=ax, pos=spring_layout(G, seed=SEED), **options)
        return fig
