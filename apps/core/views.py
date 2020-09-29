from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import (
    View, TemplateView, ListView, DetailView, FormView,
)
from django.views.generic.list import MultipleObjectMixin

from apps.core.forms import ContactUsModelForm
from apps.core.models import Category, Product


class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        product_qs = Product.objects.order_by('-created_at')[:3]
        context['product_list'] = product_qs
        return render(request, 'core/index.html', context)


class IndexTemplateView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_qs = Product.objects.order_by('-created_at')[:3]
        context['product_list'] = product_qs
        return context


# def index(request):
#     context = {}
#     product_qs = Product.objects.order_by('-created_at')[:3]
#     context['product_list'] = product_qs
#     return render(request, 'core/index.html', context)


class CategoryListView(ListView):
    template_name = 'core/category_list.html'
    queryset = Category.objects.all().order_by('?')
    context_object_name = 'categories'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['some'] = 'value'
        return context


# def category_list(request):
#     context = {}
#     category_qs = Category.objects.all()
#     context['category_list'] = category_qs
#     return render(request, 'core/category_list.html', context)


class CategoryDetailView(PermissionRequiredMixin, DetailView,
                         MultipleObjectMixin):
    permission_required = ('core.view_category', 'core.add_category')
    model = Category
    template_name = 'core/category.html'
    paginate_by = 2

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        object_list = self.get_object().products.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


def category_detail(request, slug):
    context = {}
    category = get_object_or_404(Category, slug=slug)
    context['category'] = category
    return render(request, 'core/category.html', context)


class ProductListView(ListView):
    template_name = 'core/product_list.html'
    queryset = Product.objects.all()
    paginate_by = 3

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            product_list = []
            for product in context['product_list']:
                product_list.append({
                    'title': product.title,
                    'category': product.category.title,
                    'description': product.description,
                    'price': product.price,
                    'image': product.image.url if product.image else None,
                })
            return JsonResponse({'product_list': product_list})

        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        order = self.request.GET.get('order', '-created_at')
        search = self.request.GET.get('search', '')
        return Product.objects.filter(
            title__icontains=search
        ).order_by(order)


def product_list(request):
    context = {}
    order = request.GET.get('order', '-created_at')
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    product_qs = Product.objects.filter(
        title__icontains=search
    ).order_by(order)

    paginator = Paginator(product_qs, 3)

    try:
        product_qs = paginator.page(page)
    except EmptyPage:
        product_qs = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        product_qs = paginator.page(1)

    context['product_list'] = product_qs
    context['paginator'] = paginator
    return render(request, 'core/product_list.html', context)


def product_detail(request, slug_category, pk):
    context = {}
    product = Product.objects.filter(
        pk=pk, category__slug=slug_category
    ).first()
    context['product'] = product
    return render(request, 'core/product.html', context)


class ContactUsFormView(FormView):
    form_class = ContactUsModelForm
    template_name = 'core/contact_us.html'
    success_url = reverse_lazy('core:index')

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def contact_us(request):
    context = {}

    if request.method == 'POST':
        form = ContactUsModelForm(request.POST)
        if form.is_valid():
            contactus_obj = form.save(commit=False)
            contactus_obj.email = 'some@test.test'
            contactus_obj.save()
            return HttpResponseRedirect('/')
        else:
            return JsonResponse(form.errors)
    else:
        form = ContactUsModelForm()

    context['form'] = form
    return render(request, 'core/contact_us.html', context)
