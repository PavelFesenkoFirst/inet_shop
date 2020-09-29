from django import template

from apps.core.models import Category, Contacts

register = template.Library()


@register.inclusion_tag('components/footer.html')
def footer():
    context = {}
    contact = Contacts.load()
    context['address'] = contact.address
    context['phone'] = contact.phone
    return context


@register.inclusion_tag('components/header.html', takes_context=True)
def header(context):
    context['category_list'] = Category.objects.all()
    return context


@register.inclusion_tag(
    'core/components/category_list.html', takes_context=True
)
def category_list(context):
    context['category_list'] = Category.objects.all()
    return context
