from django.shortcuts import redirect, reverse

from rolepermissions.checkers import has_role
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.accounts.roles import Admin, Subscriber, DemoUser

def admin_only(func):
    @login_required
    def check_admin(request, *args, **kwargs):
        if not has_role(request.user, Admin) and not request.user.is_superuser:
            raise PermissionDenied("You Do Not have permissions to access this page")
        
        return func(request, *args, **kwargs)
    
    return check_admin

def subscriber_only(func):
    def inner(request, *args, **kwargs):

        if is_demo_user(request.user):
            return redirect(reverse('dashboard:upgrade-required'))

        return func(request, *args, **kwargs)
    return inner

def is_demo_user(user):
    return not has_role(user, Subscriber) and not has_role(user, Admin) and not user.is_superuser