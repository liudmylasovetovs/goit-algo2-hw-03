import networkx as nx
import pandas as pd

edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

G = nx.DiGraph()
G.add_weighted_edges_from(edges, weight="capacity")
G.add_edge("Source", "Термінал 1", capacity=float('inf'))
G.add_edge("Source", "Термінал 2", capacity=float('inf'))

stores = [f"Магазин {i}" for i in range(1, 15)]
for store in stores:
    G.add_edge(store, "Sink", capacity=float('inf'))

flow_value, flow_dict = nx.maximum_flow(G, "Source", "Sink", flow_func=nx.algorithms.flow.edmonds_karp)
flow_data = []

for terminal in ["Термінал 1", "Термінал 2"]:
    for store in stores:
        total_flow = sum(flow_dict[warehouse][store] for warehouse in flow_dict[terminal] if store in flow_dict[warehouse])
        flow_data.append((terminal, store, total_flow))
flow_df = pd.DataFrame(flow_data, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])

print(flow_df)
print("Максимальний потік в мережі:", flow_value)