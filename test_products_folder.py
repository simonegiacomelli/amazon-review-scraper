from unittest import TestCase

from products_folder import ProductsFolder


class TestProductsFolder(TestCase):

    def setUp(self) -> None:
        self.target = ProductsFolder(folder='test_files/products_structure')

    def test_groups(self):
        actual = [g.name for g in self.target.groups]
        self.assertEqual(['group1', 'group2'], actual)

    def test_products_for_group(self):
        expected = ['amazonProductId1--product-title-1', 'amazonProductId2--product-title-2']
        actual = self.target.group_by_name('group1').products
        self.assertEqual(expected, actual)

        expected = []
        actual = self.target.group_by_name('group2').products
        self.assertEqual(expected, actual)
