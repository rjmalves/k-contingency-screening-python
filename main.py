import matplotlib.pyplot as plt
import seaborn as sns
import time

from screening.models.network import Network
from screening.controllers.screener import Screener
from screening.controllers.viewer import Viewer
from screening.controllers.correlator import Correlator


n = Network.from_edgelist("graphs/itaipu11.txt")
s = Screener(n)
v = Viewer(n, s)
c = Correlator(n, s)
df = c.metrics
sns.pairplot(df, diag_kind="kde")
df.to_csv("metrics_itaipu11.csv")
plt.savefig("corr.png")

ti = time.time()
k = 4
fig = v.global_deltas_graph_plot(k)
plt.savefig(f"ieee57_k{k}.png")
print(f"Tempo para calcular: {time.time() - ti:.2f} s")


networks = Network.from_graph6("graphs/4nodes2c")
screeners = [Screener(n) for n in networks]
correlators = [Correlator(n, s) for n, s in zip(networks,
                                                screeners)]

