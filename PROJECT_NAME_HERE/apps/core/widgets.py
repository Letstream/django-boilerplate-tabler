from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class ImageInput(forms.ClearableFileInput):

    template_name = 'core/forms/widgets/input-image.html'
    initial_text = _('Current')
    input_text = _('Select New')
    clear_checkbox_label = _('Remove?')


class DateTimePickerInlineInput(forms.TextInput):

    template_name = 'core/forms/widgets/datetimepickerinline.html'

    class Media:
        css = {"all": ("assets/css/bootstrap-datetimepicker.min.css",)}


class DatePickerInput(forms.TextInput):

    template_name = 'core/forms/widgets/datepicker.html'

    class Media:
        css = {"all": ("assets/css/bootstrap-datetimepicker.min.css",)}
