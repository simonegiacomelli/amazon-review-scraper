import os
from pathlib import Path


class Group:
    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.group_folder = folder / name

    @property
    def all_products(self):
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
        all = ['one_star', 'two_star', 'three_star', 'four_star', 'five_star']
        return [Star(n) for n in all]


class Star:
    def __init__(self, name):
        self.name = name


class AllProducts:
    def __init__(self, folder='products'):
        self.folder: Path = Path(folder)

    @property
    def all_groups(self):
        return [self.group_by_name(n) for n in sorted(os.listdir(self.folder))]

    def group_by_name(self, group_name) -> Group:
        res = Group(self.folder, group_name)
        return res


class BaseFolder:
    def __init__(self, folder, base=None):
        self.folder = folder
        self.base: BaseFolder = base

    @property
    def path(self):
        return self.folder if self.base is None else self.base.path + '/' + self.folder
