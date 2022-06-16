import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

from screening.models.network import Network
from screening.controllers.screener import ExhaustiveScreener
from screening.controllers.viewer import Viewer
from screening.controllers.correlator import Correlator


n = Network.from_edgelist("graphs/ieee39.txt")
s = ExhaustiveScreener(n)
s.global_deltas(2)
v = Viewer(n, s)
c = Correlator(n, s)
df = c.metrics
df.to_csv("metrics_ieee39.csv")
df_nonzero = df.loc[df["DeltaCFBk1"] > 0, :]
sns.pairplot(df_nonzero, diag_kind="kde")
plt.savefig("corr_ieee39.png")

ti = time.time()
k = 4
fig = v.global_deltas_graph_plot(k)
plt.savefig(f"ieee57_k{k}.png")
print(f"Tempo para calcular: {time.time() - ti:.2f} s")

n = 7
networks = Network.from_graph6(f"graphs/{n}nodes2c.g6")
screeners = [ExhaustiveScreener(n, num_processors=6) for n in networks]
correlators = [Correlator(n, s) for n, s in zip(networks,
                                                screeners)]
df = None
for i, c in enumerate(correlators):
    print(i)
    df_c = c.metrics
    if df is None:
        df = df_c
    else:
        df = pd.concat([df, df_c], ignore_index=True)

sns.pairplot(df, diag_kind="kde")
plt.savefig(f"corr_2c_{n}nodes.png")
df.to_csv(f"corr_2c_{n}nodes.csv")
