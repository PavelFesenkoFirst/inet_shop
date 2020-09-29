from django.views.generic import View, TemplateView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from apps.core.models import Product
from apps.order.cart import Cart
from apps.order.models import OrderProduct
from apps.order.forms import OrderForm


class CartTemplateView(TemplateView):
    template_name = 'order/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        print(len(context['cart']))
        return context


class CartAddView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.add(product)
        return redirect('core:product-list')


class CartRemoveView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.remove(product)
        return redirect('order:cart')


class CartClearView(RedirectView):
    pattern_name = 'core:index'

    def get_redirect_url(self, *args, **kwargs):
        Cart(self.request).clear()
        return super().get_redirect_url(*args, **kwargs)


class CheckoutTemplateView(TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            form_params = request.POST.copy()
            form_params.update({
                'user': request.user,
                'name': request.user.name,
                'surname': request.user.surname,
                'phone': request.user.phone,
                'email': request.user.email,
            })
            form = OrderForm(form_params)
        else:
            form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()
            cart = Cart(request)
            for item in cart:
                OrderProduct.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )
            cart.clear()
        else:
            return JsonResponse(form.errors)

        return redirect('core:index')
