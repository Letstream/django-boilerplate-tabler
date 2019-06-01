from datetime import datetime, timedelta

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.roles import assign_role, clear_roles, get_user_roles

from apps.accounts import roles as r
from apps.accounts.forms import UserSignupForm
from apps.accounts.models import User
from apps.accounts.roles import Admin, Subscriber
from apps.accounts.utils import DoPostAccountCreation, getTableDataForUsers
from apps.core.constants import database_keys as dk
from apps.core.constants import permissions as p
from apps.core.utils import getOption, getOptions, setOption
from apps.email.models import EmailQueue

from .forms import OptionsForm, PasswordChangeForm, RolesForm, UserForm
from .utils import TableData as td


@login_required
def IndexView(request):

    t = timezone.now()
    if has_role(request.user, Admin) or request.user.is_superuser:
        context = {
            "count": {
                "users": User.objects.all().count(),
                "inactive_users": User.objects.filter(is_active=False).count(),
                "online_users": User.objects.filter(last_active__gte=timezone.now() - timezone.timedelta(seconds=300)).count(),
                "unconfirmed_emails": User.objects.filter(email_confirmed=False).count(),
                "users_joined_this_month": User.objects.filter(date_joined__gte = t.date()-timedelta(t.day)).count(),
                "users_joined_previous_month": User.objects.filter(date_joined__range= [t.date()-timedelta(t.day+30), t.date()-timedelta(t.day)]).count(),
                "users_joined_this_week":User.objects.filter(date_joined__range =[t.date()-timedelta(t.isoweekday()), t.date()]).count(),
                "users_joined_previous_week": User.objects.filter(date_joined__range = [t.date()-timedelta(t.isoweekday()+7), t.date()-timedelta(t.isoweekday())]).count(),
                "users_joined_today": User.objects.filter(date_joined = t.date()).count(),
                "users_joined_yesterday": User.objects.filter(date_joined=t.date()-timedelta(1)).count(),
                "tasks": {
                    "emails": {
                        "pending": EmailQueue.objects.filter(status=EmailQueue.PENDING).count(),
                        "ongoing": EmailQueue.objects.filter(status=EmailQueue.SENDING).count()
                    }
                }
            }
        }
        return render(request, "dashboard/index.html", {"data": context})
    else:
        context = {}
        return render(request, "dashboard/index-subscriber.html", {"data": context})

@login_required
def BrowseUsersView(request):
    if has_permission(request.user, p.READ_USERS):
        enabled_columns = None
        if request.GET.get('enabled_columns', False):
            enabled_columns = request.GET.getlist('enabled_columns')
        sort_by = request.GET.get('sort_by', None)
        sort_order = request.GET.get('sort_order', None)
        search = request.GET.get('search', None)
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pagesize', 20))

        try:
            tableData = getTableDataForUsers(
                request_obj=request.GET.urlencode(),
                page = page,
                enabled_columns=enabled_columns,
                search=search,
                sort_by=sort_by,
                sort_order=sort_order,
                page_size=page_size,
                admin_view=True
            )
        except td.PageIndexOutOfRangeError:
            raise Http404("Page not found")

        return render(request, "dashboard/list.html", {"tableData": tableData, 'title': "Browse Users"})
    else:
        raise PermissionDenied("You are not allowed to List Users.")


@login_required
def UserEditView(request, userid=None):

    form = None
    user = None
    passForm = None
    rolesForm = None

    if userid == None:
        user = request.user
    elif has_permission(request.user, p.EDIT_USERS) or request.user.id == userid:
        try:
            user = User.objects.get(id=userid)
        except ObjectDoesNotExist as e:
            raise Http404("User Does Not Exist")
    else:
        raise PermissionDenied(
            "You do not have permission to edit/view this user")

    if has_permission(request.user, p.EDIT_USERS):
        roles = []
        for x in get_user_roles(user):
            roles.append(x.display_name)
        rolesForm = RolesForm({'roles': roles})

    form = UserForm(user=request.user, instance=user)
    passForm = PasswordChangeForm(user)

    if request.method == "POST":
        if 'user-submit' in request.POST:
            form = UserForm(user=request.user, data=request.POST or None,
                            files=request.FILES or None, instance=user)
            if form.is_valid():
                form.save()

        if 'password-change' in request.POST:
            passForm = PasswordChangeForm(user, request.POST or None)
            if passForm.is_valid():
                passForm.save()
                update_session_auth_hash(request, user)

        if 'change-role' in request.POST:
            rolesForm = RolesForm(request.POST or None)
            if rolesForm.is_valid():
                user.change_user_role(rolesForm.cleaned_data['roles'])

    return render(request, "dashboard/edit-user.html", {'form': form, 'user_context': user, 'passform': passForm, 'rolesForm': rolesForm})

@login_required
def UserCreationView(request):

    if not has_role(request.user, Admin) and not request.user.is_superuser:
        raise PermissionDenied("You do not have permissions to acess this page!")

    form = None
    if request.method == "POST":
        form = UserSignupForm(data=request.POST or None, files=request.FILES or None, is_admin=True)
        if form.is_valid():
            user = form.save()
            DoPostAccountCreation(user)
            return redirect(reverse('dashboard:list-users'))
    else:
        form = UserSignupForm(is_admin=True)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Create New User'})

@login_required
def ManageSiteView(request):
    if not request.user.is_superuser:
        raise PermissionDenied(
            "You do not have permissions to access this page!")

    form = None
    if request.method == "POST":
        form = OptionsForm(data = request.POST, files = request.FILES or None)
        if form.is_valid():
            for data in form.cleaned_data:
                setOption(data, form.cleaned_data[data])
    else:
        form = OptionsForm(initial=getOptions())
    return render(request, "dashboard/settings.html", {"form": form})
