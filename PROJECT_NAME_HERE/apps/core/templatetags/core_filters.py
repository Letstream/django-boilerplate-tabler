from django import template
from apps.core.decorators import is_demo_user
register = template.Library()

@register.filter(name='check_subscriber')
def check_subscriber(user):
    return is_demo_user(user)
