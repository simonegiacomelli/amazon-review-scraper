import os
from pathlib import Path


class Group:
    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.group_folder = folder / name

    @property
    def products(self):  # rename to all_products
        listdir = [p for p in os.listdir(self.group_folder)
                   if not p.startswith('.') and (self.group_folder / p).is_dir()]
        return sorted(listdir)

    def product_by_name(self, product_name):
        return Product(self, product_name)


class Product:
    def __init__(self, group: Group, product_name):
        self.group = group
        self.product_name = product_name

    @property
    def all_stars(self):
        return [0] * 5


class ProductsFolder:
    def __init__(self, folder='products'):
        self.folder: Path = Path(folder)

    @property
    def all_groups(self):
        return [self.group_by_name(n) for n in sorted(os.listdir(self.folder))]

    def group_by_name(self, group_name) -> Group:
        res = Group(self.folder, group_name)
        return res
