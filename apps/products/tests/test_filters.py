from django.test import TestCase

from apps.products.filters import ProductFilter

from .factories import (
    ProductFactory,
    ProductVariantFactory,
    CategoryFactory,
    BrandFactory,
)


class ProductFilterTest(TestCase):

    def setUp(self):
        self.category1 = CategoryFactory()
        self.category2 = CategoryFactory()

        self.brand1 = BrandFactory()
        self.brand2 = BrandFactory()

        self.product1 = ProductFactory(
            category=self.category1,
            brand=self.brand1,
        )

        self.product2 = ProductFactory(
            category=self.category2,
            brand=self.brand2,
        )

        ProductVariantFactory(
            product=self.product1,
            color="black",
            size="42",
            price=100,
            stock=10,
        )

        ProductVariantFactory(
            product=self.product2,
            color="white",
            size="43",
            price=200,
            stock=0,
        )
    def test_filter_by_category(self):
        queryset = ProductFilter(
            {
                "category": self.category1.id,
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )
    def test_filter_by_brand(self):
        queryset = ProductFilter(
            {
                "brand": self.brand2.id,
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product2,
        )

    def test_filter_by_color(self):
        queryset = ProductFilter(
            {
                "color": "black",
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product1,
        )

    def test_filter_by_size(self):
        queryset = ProductFilter(
            {
                "size": "43",
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product2,
        )

    def test_filter_by_min_price(self):
        queryset = ProductFilter(
            {
                "min_price": 150,
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product2,
        )

    def test_filter_by_max_price(self):
        queryset = ProductFilter(
            {
                "max_price": 150,
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product1,
        )

    def test_filter_in_stock(self):
        queryset = ProductFilter(
            {
                "in_stock": True,
            },
            queryset=ProductFactory._meta.model.objects.all(),
        ).qs

        self.assertEqual(
            queryset.first(),
            self.product1,
        )