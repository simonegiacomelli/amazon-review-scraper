from unittest import TestCase

from products_folder import ProductsFolder


class TestProductsFolder(TestCase):

    def setUp(self) -> None:
        self.target = ProductsFolder(folder='test_files/products_structure')

    def test_groups(self):
        actual = [g.name for g in self.target.all_groups]
        self.assertEqual(['group1', 'group2'], actual)

    def test_products_for_group(self):
        expected = ['amazonProductId1--product-title-1', 'amazonProductId2--product-title-2']
        actual = self.target.group_by_name('group1').products
        self.assertEqual(expected, actual)

        expected = []
        actual = self.target.group_by_name('group2').products
        self.assertEqual(expected, actual)

    def test_get_star_folders_for_product(self):
        group1 = self.target.group_by_name('group1')
        product1 = group1.product_by_name('amazonProductId1--product-title-1')
        self.assertEqual(5, len(product1.all_stars))

        product2 = group1.product_by_name('amazonProductId2--product-title-2')
        self.assertEqual(5, len(product2.all_stars))
