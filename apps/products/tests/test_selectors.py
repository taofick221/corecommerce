from django.core.cache import cache
from django.test import TestCase

from apps.products.selectors import get_brands, get_categories

from .factories import BrandFactory, CategoryFactory


class ProductSelectorTest(TestCase):

    def setUp(self):
        cache.clear()

    def test_get_categories(self):
        CategoryFactory()

        categories = get_categories()

        self.assertEqual(
            len(categories),
            1,
        )

    def test_get_brands(self):
        BrandFactory()

        brands = get_brands()

        self.assertEqual(
            len(brands),
            1,
        )

    def test_categories_returns_queryset_data(self):
        category = CategoryFactory()

        categories = get_categories()

        self.assertIn(
            category,
            categories,
        )

    def test_brands_returns_queryset_data(self):
        brand = BrandFactory()

        brands = get_brands()

        self.assertIn(
            brand,
            brands,
        )
