from django.urls import path

from apps.order.views import (
    CartTemplateView, CartAddView, CartRemoveView, CartClearView,
    CheckoutTemplateView,
)

app_name = 'order'

urlpatterns = [
    path('cart/', CartTemplateView.as_view(), name='cart'),
    path('add/<pk>/', CartAddView.as_view(), name='cart-add'),
    path('remove/<pk>/', CartRemoveView.as_view(), name='cart-remove'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
    path('checkout/', CheckoutTemplateView.as_view(), name='checkout'),
]
