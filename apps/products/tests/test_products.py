from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.products.models import Product,ProductImage,ProductVariant,Category,Brand


class ProductAPITest(APITestCase):
    def setUp(self):
        self.admin=User.objects.create_superuser(
            email="admin@test.com",
            password="Admin123@",
        )
        self.user=User.objects.create_user(
            email="user@test.com",
            password="User123@",
        )
        self.category=Category.objects.create(
            name="Shoes",
        )
        self.brand=Brand.objects.create(
            name="Nike",
        )
        self.product=Product.objects.create(
            name="Nike Air Max",
            description="Running Shoe",
            category=self.category,
            brand=self.brand,
            is_active=True,
        )
        ProductVariant.objects.create(
             product=self.product,
            size="42",
            color="Black",
            price=120,
            stock=10,
            sku="SKU001",
            is_default=True,
        )
        ProductImage.objects.create(
            product=self.product,
            is_primary=True,
        )
        self.list_url=reverse("products-list")
        self.detail_url=reverse(
            "products-detail",
            kwargs={
                "slug":self.product.slug,
            },
        )
    def test_product_list(self):
        response=self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
    def test_product_detail(self):
        response=self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["name"],
            self.product.name,
        )
    
    def test_anonymous_cannot_create_product(self):
        payload = {
            "name": "Adidas Samba",
            "description": "Test Product",
            "category": self.category.id,
            "brand": self.brand.id,
            "variants": [
                {
                    "size": "42",
                    "color": "White",
                    "price": 100,
                    "stock": 5,
                    "sku": "SKU100",
                    "is_default": True,
                }
            ],
            "images": [],
        }
        response=self.client.post(
            self.list_url,
            payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
    def test_user_cannot_create_product(self):
        self.client.force_authenticate(
            self.user,
        )

        payload = {
            "name": "Adidas Samba",
            "description": "Test Product",
            "category": self.category.id,
            "brand": self.brand.id,
            "variants": [
                {
                    "size": "42",
                    "color": "White",
                    "price": 100,
                    "stock": 5,
                    "sku": "SKU100",
                    "is_default": True,
                }
            ],
            "images": [],
        }
        response=self.client.post(
            self.list_url,
            payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    def test_admin_can_create_product(self):
        self.client.force_authenticate(
            self.admin,
        )
        payload = {
            "name": "Adidas Samba",
            "description": "Test Product",
            "category": self.category.id,
            "brand": self.brand.id,
            "variants": [
                {
                    "size": "42",
                    "color": "White",
                    "price": 100,
                    "stock": 5,
                    "sku": "SKU100",
                    "is_default": True,
                }
            ],
            "images": [],
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Product.objects.count(),
            2,
        )
        self.assertTrue(
            Product.objects.filter(
                name="Adidas Samba",
            ).exists()
        )
    def test_admin_can_update_product(self):
        self.client.force_authenticate(
        self.admin,
        )

        payload = {
        "name": "Nike Air Max Updated",
        "description": "Updated Product",
        "category": self.category.id,
        "brand": self.brand.id,
        "variants": [
            {
                "id": self.product.variants.first().id,
                "size": "43",
                "color": "Black",
                "price": 150,
                "stock": 20,
                "sku": "SKU001",
                "is_default": True,
            }
        ],
        "images": [
            {
                "id": self.product.images.first().id,
                "is_primary": True,
            }
        ],
        }

        response = self.client.put(
        self.detail_url,
        payload,
        format="json",
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
        self.product.name,
        "Nike Air Max Updated",
        )
    def test_user_cannot_update_product(self):
        self.client.force_authenticate(
        self.user,
        )

        payload = {
        "name": "Updated",
        }

        response = self.client.patch(
        self.detail_url,
        payload,
        format="json",
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN,
        )