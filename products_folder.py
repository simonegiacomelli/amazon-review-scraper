import os
from pathlib import Path


class Group:
    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.group_folder = folder / name

    @property
    def products(self):
        listdir = [p for p in os.listdir(self.group_folder)
                   if not p.startswith('.') and (self.group_folder / p).is_dir()]
        return sorted(listdir)


class ProductsFolder:
    def __init__(self, folder='products'):
        self.folder: Path = Path(folder)

    @property
    def groups(self):
        return [self.group_by_name(n) for n in sorted(os.listdir(self.folder))]

    def group_by_name(self, group_name):
        res = Group(self.folder, group_name)
        return res
