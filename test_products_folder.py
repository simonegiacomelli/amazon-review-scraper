from unittest import TestCase

from products_folder import ProductsFolder


class TestProductsFolder(TestCase):

    def setUp(self) -> None:
        self.target = ProductsFolder(folder='test_files/products_structure')

    def test_groups(self):
        self.assertEqual(['group1', 'group2'], self.target.groups)

    def test_products_for_group(self):
        expected = ['amazonProductId1--product-title-1', 'amazonProductId2--product-title-2']
        actual = self.target.products_for_group('group1')
        self.assertEqual(expected, actual)

        expected = []
        actual = self.target.products_for_group('group2')
        self.assertEqual(expected, actual)
