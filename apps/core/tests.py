import json

from django.test import TestCase, RequestFactory

from apps.core.models import Category, Product
from apps.api.v1.views import ProductDetailView


class TestModel(TestCase):

    def setUp(self):
        category = Category.objects.create(title='категория 1')
        Product.objects.create(
            category=category,
            title='product 1',
            price=10000,
            discount=10
        )

    def test_category(self):
        category = Category.objects.first()
        self.assertEqual(category.slug, 'kategoriya-1')

    def test_product(self):
        product = Product.objects.first()
        self.assertEqual(product.actual_price, 9000)

