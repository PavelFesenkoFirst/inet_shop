from django.urls import path

from apps.core.views import (
    category_detail, product_list, product_detail,
    contact_us,
    IndexView, IndexTemplateView, CategoryListView, CategoryDetailView,
    ContactUsFormView, ProductListView
)

app_name = 'core'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug>/', CategoryDetailView.as_view(),
         name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug_category>/<pk>/', product_detail, name='product-detail'),
    path('contact_us/', ContactUsFormView.as_view(), name='contact-us'),
]
