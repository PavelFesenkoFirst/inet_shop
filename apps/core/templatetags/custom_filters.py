from django import template

register = template.Library()


@register.filter
def cut_filter(value, arg):
    return value.replace(arg, '')


@register.filter
def formatted_phone(value):
    return '+' + value


@register.inclusion_tag('components/footer.html')
def footer():
    context = {}
    context['phone'] = '380661234567'
    return context
