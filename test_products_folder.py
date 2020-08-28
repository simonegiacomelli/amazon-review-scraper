from unittest import TestCase

from products_folder import ProductsFolder


class TestProductsFolder(TestCase):

    def test_groups(self):
        target = ProductsFolder(folder='test_files/products_structure')
        self.assertEqual(['group1', 'group2'], target.groups)

    def test_products_for_group(self):
        target = ProductsFolder(folder='test_files/products_structure')

        expected = ['amazonProductId1--product-title-1', 'amazonProductId2--product-title-2']
        actual = target.products_for_group('group1')
        self.assertEqual(expected, actual)

        expected = []
        actual = target.products_for_group('group2')
        self.assertEqual(expected, actual)


