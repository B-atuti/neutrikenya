from django import template
from urllib.parse import urlencode
from django.utils.http import urlencode

register = template.Library()

@register.filter
def remove_query(query_string, key):
    """Remove a query parameter from a URL query string."""
    if not query_string:
        return ''
    params = {}
    for param in query_string.split('&'):
        if '=' in param:
            k, v = param.split('=', 1)
            if k != key:
                params[k] = v
    return urlencode(params)

@register.simple_tag
def query_transform(request, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs from the kwargs dict.
    """
    updated = request.GET.copy()
    
    # Remove parameters set to None
    for key, value in kwargs.items():
        if value is None and key in updated:
            updated.pop(key)
        elif value is not None:
            updated[key] = value
    
    return urlencode(updated) 