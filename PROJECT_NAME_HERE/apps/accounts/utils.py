from django.contrib.auth.tokens import (PasswordResetTokenGenerator,
                                        default_token_generator)
from django.db.models.fields.reverse_related import ManyToOneRel, OneToOneRel
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils import six
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rolepermissions.roles import assign_role

from apps.core.utils import getOption
from apps.dashboard.utils import TableData
from apps.email.schedulers import ScheduleEmail

from .models import User
from .roles import DemoUser, Subscriber


def UserExistsByEmail(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return False


def sendPasswordResetEmail(user_email):

    user = UserExistsByEmail(user_email)
    if not user:
        return False

    context = {
        'user': user,
        'domain': getOption('site_url'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': PasswordResetTokenGenerator().make_token(user),
        'protocol': 'http'
    }

    subject = "Reset your Password"

    html = render_to_string(
        "accounts/email/forgot-password/template.html", context=context)
    text = render_to_string(
        "accounts/email/forgot-password/template.txt", context=context)

    ScheduleEmail(to_email=user.email, subject=subject,
                  html_text=html, plain_text=text)

    return True


def ActivateUserAccount(user):
    try:
        user.email_confirmed = True
        user.save()
        return True
    except Exception:
        return False


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email_confirmed)
        )


def SendAccountActivationEmail(user_email):

    user = UserExistsByEmail(user_email)
    if not user:
        return False

    context = {
        'user': user,
        'domain': getOption('site_url'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': AccountActivationTokenGenerator().make_token(user)
    }

    subject = "Activate your account"

    html = render_to_string(
        "accounts/email/signup/template.html", context=context)
    text = render_to_string(
        "accounts/email/signup/template.txt", context=context)

    ScheduleEmail(to_email=user.email, subject=subject,
                  html_text=html, plain_text=text)

    context = {
        'user': user
    }
    html = render_to_string(
        "accounts/email/signup-admin/template.html", context=context)
    text = render_to_string(
        "accounts/email/signup-admin/template.txt", context=context)

    ScheduleEmail(to_email=getOption('new_account_email_to_address'),
                  subject="New User Signup at GSTHEALTH", html_text=html, plain_text=text)

    return True


def getTableDataForUsers(request_obj, page=1, enabled_columns=None, search=None, sort_by=None, sort_order=None, page_size=20, admin_view=False, custom_button=False, custom_button_label="", custom_button_namespace="", custom_button_kwargs={}):
    t = TableData()
    users, start_index, total_count = User.filter_user_data(
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )

    if start_index >= total_count:
        raise t.PageIndexOutOfRangeError()

    t.addMetaField('pagination', {
        "page": page,
        "page_size": page_size,
        "total": total_count,
        "start": start_index+1,
        "end": start_index+len(users),
        "next_url": "",
        "prev_url": ""
    })
    t.meta['pagination']['prev_url'], t.meta['pagination']['next_url'] = t.getPaginationUrl(
        request_obj)

    if search != None:
        t.addMetaField("search", search)

    if sort_by != None:
        t.addMetaField("sorted_by", sort_by)
        t.addMetaField("sort_order", sort_order)

    if enabled_columns == None:
        t.addField("avatar", "...", "w-1")
        t.addField("first_name", "First Name")
        t.addField("last_name", "Last Name")
        t.addField("email", "Email")
    else:
        for col in enabled_columns:
            field = User._meta.get_field(col)
            if field.name == "avatar":
                label = "..."
            else:
                label = field.verbose_name
            t.addField(field.name, label)

    ignored_fields = ['password', 'groups', 'user_permissions', 'is_superuser']
    non_sortable_fields = ignored_fields + ['avatar']
    for field in User._meta.get_fields():
        if type(field) != ManyToOneRel and type(field) != OneToOneRel:
            if field.name not in ignored_fields:
                t.addAvailableField(field.name, field.verbose_name)
            if field.name not in non_sortable_fields:
                t.addSortableField(field.name, field.verbose_name)

    counter = 0
    for user in users:
        t.addRow(user.id)

        if enabled_columns == None:

            t.addCellToRow(counter, "avatar", "", "", {
                           "url": user.avatar.url if user.avatar else "", 'is_online': user.is_online()})
            t.addCellToRow(counter, 'text', user.first_name)
            t.addCellToRow(counter, 'text', user.last_name)
            t.addCellToRow(counter, "text-secondary", user.email)
        else:
            for col in enabled_columns:
                field = User._meta.get_field(col)
                param = {}
                cell_type = ""
                text = ""
                subtext = ""
                if field.name == "avatar":
                    param = {"url": user.avatar.url if user.avatar else ""}
                    cell_type = "avatar"
                else:
                    text = getattr(user, field.name)
                    cell_type = "text"

                t.addCellToRow(counter, cell_type, text, subtext, param)

        if admin_view:
            t.addActionButtonToRow(counter, reverse(
                'dashboard:edit-user', args=[user.id]), "Edit", "btn-secondary")

            if user.is_active:
                t.addActionButtonToRow(counter, reverse(
                    'dashboard:suspend-user', args=[user.id]), "Suspend", "btn-danger")
            else:
                t.addActionButtonToRow(counter, reverse(
                    'dashboard:enable-user', args=[user.id]), "Enable", "btn-primary")

            t.addActionButtonToRow(counter, reverse('accounts:loginas', args=[
                                   user.id]), "Login As", "btn-primary")

        if custom_button:
            kwargs = custom_button_kwargs
            custom_button_kwargs['userid'] = user.id
            t.addActionButtonToRow(counter, reverse(
                custom_button_namespace, kwargs=custom_button_kwargs), custom_button_label, "btn-secondary")

        counter += 1

    return t.getObject()


def DoPostAccountCreation(user):
    assign_role(user, Subscriber)

    #Add more tasks here
