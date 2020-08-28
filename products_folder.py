import os
from pathlib import Path


class ProductsFolder:
    def __init__(self, folder='products'):
        self.folder: Path = Path(folder)

    @property
    def groups(self):
        return sorted(os.listdir(self.folder))

    def products_for_group(self, group):
        group_folder = self.folder / group
        listdir = [p for p in os.listdir(group_folder) if not p.startswith('.') and (group_folder / p).is_dir()]
        return sorted(listdir)
