from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from django import forms
from django.contrib.auth.forms import AdminPasswordChangeForm
from rolepermissions.checkers import has_permission

from apps.accounts.models import User
from apps.core.constants import permissions as p
from apps.accounts.roles import Subscriber, Admin, DemoUser


class UserForm(forms.ModelForm):

    gender = forms.ChoiceField(
        choices=User.gender_choices,
        widget=forms.RadioSelect
    )

    mobile = forms.CharField(
        label="Mobile Number"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender',
                  'avatar', 'mobile']

    def __init__(self, user, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "container"
        self.helper.label_class = "font-weight-bold"
        edit_sensitive_fields = True if has_permission(
            user, p.EDIT_USERS) else False

        emailField = Field('email')

        if not edit_sensitive_fields:
            emailField = Field('email', readonly=edit_sensitive_fields)

        self.helper.layout = Layout(
            Div(
                Field('first_name', wrapper_class='col-12 col-md-6'),
                Field('last_name', wrapper_class='col-12 col-md-6'),
                css_class="row"
            ),
            emailField,
            Field('mobile'),
            InlineRadios('gender'),
            'avatar'
        )
        self.helper.add_input(Submit('user-submit', 'Save'))


class PasswordChangeForm(AdminPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.pop("autofocus", None)

        self.helper = FormHelper()
        self.helper.label_class = "font-weight-bold"

        self.helper.add_input(Submit('password-change', 'Change Password'))


class RolesForm(forms.Form):

    roles = forms.MultipleChoiceField(
        choices=(
            (Subscriber.display_name, Subscriber.title),
            (Admin.display_name, Admin.title),
            (DemoUser.display_name, DemoUser.title)
        )
    )

    def __init__(self, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.label_class = "font-weight-bold"

        self.helper.add_input(Submit('change-role', 'Save Role(s)'))


class OptionsForm(forms.Form):

    site_title = forms.CharField(label="Site Title", required=False)
    site_description = forms.CharField(
        label="Site Description", required=False)
    support_email = forms.EmailField(label="Support Email", required=False)
    site_url = forms.URLField(label="Site URL", required=True)
    smtp_server = forms.CharField(label="SMTP Server")
    smtp_user = forms.CharField(label="SMPT User")
    smtp_pass = forms.CharField(label="SMTP Password")
    smtp_port = forms.CharField(label="SMTP Port")
    send_mails_as = forms.CharField(max_length=1000, label="Send Email As")

    new_account_email_to_address = forms.EmailField(
        label='New Account Email Notification To')

    def __init__(self, *args, **kwargs):
        super(OptionsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.label_class = "font-weight-bold"

        self.helper.layout = Layout(
            Div(
                'site_title',
                'site_url',
                'site_description',
                'support_email',
                'new_account_email_to_address',
                css_class="card my-3 my-md-5 p-3"
            ),
            Div(
                'smtp_server',
                'smtp_user',
                'smtp_pass',
                'smtp_port',
                'send_mails_as',
                css_class="card my-3 my-md-5 p-3"
            )
        )

        self.helper.add_input(Submit('save-options', 'Save Options'))
