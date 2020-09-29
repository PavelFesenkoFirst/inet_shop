from django import forms

from apps.order.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('complete',)
