import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import pandas as pd

# Функція для реалізації BFS у алгоритмі Едмондса-Карпа
def bfs(capacity, flow, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        node = queue.popleft()
        for neighbor in capacity[node]:
            if neighbor not in visited and capacity[node][neighbor] - flow[node][neighbor] > 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = node
                if neighbor == sink:
                    return True
    return False

# Функція для знаходження максимального потоку алгоритмом Едмондса-Карпа
def edmonds_karp(capacity, source, sink):
    flow = {u: {v: 0 for v in capacity[u]} for u in capacity}  # Початковий потік = 0
    max_flow = 0
    parent = {}

    while bfs(capacity, flow, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow, flow

# Визначення ребер з пропускною здатністю
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
    ("Склад 4", "Магазин 14", 10)
]

# Побудова матриці потужностей
capacity = {}
for u, v, c in edges:
    if u not in capacity:
        capacity[u] = {}
    if v not in capacity:
        capacity[v] = {}
    capacity[u][v] = c
    capacity[v][u] = 0  # Зворотні ребра для залишкової мережі

# Додавання джерела та стоку
capacity["Джерело"] = {"Термінал 1": float("inf"), "Термінал 2": float("inf")}
capacity["Термінал 1"]["Джерело"] = 0
capacity["Термінал 2"]["Джерело"] = 0
capacity["Сток"] = {}

for i in range(1, 15):
    shop = f"Магазин {i}"
    if shop not in capacity:
        capacity[shop] = {}
    capacity[shop]["Сток"] = float("inf")
    capacity["Сток"][shop] = 0

# Виконання алгоритму
max_flow, flow_result = edmonds_karp(capacity, "Джерело", "Сток")

# Створення таблиці фактичних потоків між терміналами та магазинами
data = []
for terminal in ["Термінал 1", "Термінал 2"]:
    for i in range(1, 15):
        shop = f"Магазин {i}"
        flow = sum(flow_result[terminal].get(warehouse, 0) for warehouse in capacity[terminal] if warehouse in flow_result and shop in flow_result[warehouse])
        data.append([terminal, shop, flow])

df = pd.DataFrame(data, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])
print(df)

# Вивід результатів
print(f"Максимальний потік у мережі: {max_flow}")