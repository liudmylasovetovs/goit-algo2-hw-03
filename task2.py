import timeit
import pandas as pd
from BTrees.OOBTree import OOBTree

file_path = "generated_items_data.csv"

try:
    data = pd.read_csv(file_path, dtype={"ID": int, "Name": str, "Category": str, "Price": float})
except FileNotFoundError:
    raise Exception(f"Error: The file {file_path} was not found.")

items = [
    (int(row["ID"]), {"Name": row["Name"], "Category": row["Category"], "Price": float(row["Price"])})
    for _, row in data.iterrows()
]

oob_tree = OOBTree()
dictionary = {}

def add_item_to_tree(tree, item_id, item_data):
    tree[item_id] = item_data

def add_item_to_dict(d, item_id, item_data):
    d[item_id] = item_data

for item_id, item_data in items:
    add_item_to_tree(oob_tree, item_id, item_data)
    add_item_to_dict(dictionary, item_id, item_data)

def range_query_tree(tree, min_price, max_price):
    return list(tree.items(min_price, max_price))

def range_query_dict(d, min_price, max_price):
    return [(key, value) for key, value in d.items() if min_price <= value["Price"] <= max_price]

min_price = 50
max_price = 150

tree_time = timeit.timeit(lambda: range_query_tree(oob_tree, min_price, max_price), number=100)
dict_time = timeit.timeit(lambda: range_query_dict(dictionary, min_price, max_price), number=100)

results = {
    "Total range_query time for OOBTree": f"{tree_time:.6f} seconds",
    "Total range_query time for Dict": f"{dict_time:.6f} seconds"
}

for key, value in results.items():
    print(f"{key}: {value}")