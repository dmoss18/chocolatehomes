from django import template
from google.appengine.api import users

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__.lower()

@register.filter
def get_logout_url(path):
    return users.create_logout_url(path)

@register.filter
def get_login_url(request):
    return users.create_login_url('dashboard.html')
