import csv
import timeit
from BTrees.OOBTree import OOBTree

# Функція для завантаження даних з CSV-файлу
def load_data(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['ID'] = int(row['ID'])
            row['Price'] = float(row['Price'])
            data.append(row)
    return data

# Функція для додавання товарів у OOBTree
def add_item_to_tree(tree, item):
    tree[item['ID']] = item

# Функція для додавання товарів у dict
def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

# Функція для виконання діапазонного запиту у OOBTree
def range_query_tree(tree, min_price, max_price):
    return [item for _, item in tree.items() if min_price <= item['Price'] <= max_price]

# Функція для виконання діапазонного запиту у dict
def range_query_dict(dictionary, min_price, max_price):
    return [item for item in dictionary.values() if min_price <= item['Price'] <= max_price]

# Основний код
filename = 'generated_items_data.csv'  # Шлях до файлу даних
data = load_data(filename)

oob_tree = OOBTree()
dictionary = {}

# Додавання товарів у структури
tree_add_time = timeit.timeit(lambda: [add_item_to_tree(oob_tree, item) for item in data], number=1)
dict_add_time = timeit.timeit(lambda: [add_item_to_dict(dictionary, item) for item in data], number=1)

# Вимірювання часу виконання діапазонних запитів
min_price, max_price = 10.0, 50.0

tree_query_time = timeit.timeit(lambda: range_query_tree(oob_tree, min_price, max_price), number=100)
dict_query_time = timeit.timeit(lambda: range_query_dict(dictionary, min_price, max_price), number=100)

# Виведення результатів
print(f'Total range_query time for OOBTree: {tree_query_time:.6f} seconds')
print(f'Total range_query time for Dict: {dict_query_time:.6f} seconds')