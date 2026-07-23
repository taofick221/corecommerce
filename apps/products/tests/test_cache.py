from django.core.cache import cache
from django.test import TestCase

from apps.products.selectors import (BRAND_CACHE_KEY, CATEGORY_CACHE_KEY,
                                     get_brands, get_categories)

from .factories import BrandFactory, CategoryFactory


class ProductCacheTest(TestCase):

    def setUp(self):
        cache.clear()

        self.category = CategoryFactory()
        self.brand = BrandFactory()

    def test_get_categories_cache_miss(self):
        categories = get_categories()

        self.assertEqual(
            len(categories),
            1,
        )

        self.assertIsNotNone(
            cache.get(
                CATEGORY_CACHE_KEY,
            )
        )

    def test_get_categories_cache_hit(self):
        get_categories()

        CategoryFactory()

        categories = get_categories()

        self.assertEqual(
            len(categories),
            1,
        )

    def test_get_brands_cache_miss(self):
        brands = get_brands()

        self.assertEqual(
            len(brands),
            1,
        )

        self.assertIsNotNone(
            cache.get(
                BRAND_CACHE_KEY,
            )
        )

    def test_get_brands_cache_hit(self):
        get_brands()

        BrandFactory()

        brands = get_brands()

        self.assertEqual(
            len(brands),
            1,
        )
