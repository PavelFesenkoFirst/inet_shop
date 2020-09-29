from django.urls import path

from rest_framework import routers

from apps.api.v1.views import (
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register(r'product-viewset', ProductViewSet)

urlpatterns = [
    path('product/', ProductCreateView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('product/all/', ProductListView.as_view()),
    path('product-viewset2/list/', ProductViewSet.as_view({'get': 'list'})),
    path('product-viewset2/<pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
] + router.urls
