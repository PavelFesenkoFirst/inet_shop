from django import template

from apps.core.models import Contacts

register = template.Library()


@register.simple_tag(takes_context=True)
def get_title(context, param, text):
    contact = Contacts.load()
    return contact.title


@register.simple_tag
def url_replace(request, **kwargs):
    query = request.GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()
