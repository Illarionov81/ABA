from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from .models import PROGRAM_STATUS_CHOICES, Program

default_status = PROGRAM_STATUS_CHOICES[0][0]

BROWSER_DATETIME_FORMAT = '%d-%m-%Y'


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatepicker_widget.html'


class ProgramForm(forms.ModelForm):
    start_date = forms.DateField(label='Дата Создания',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=XDatepickerWidget)

    end_date = forms.DateField(required=False,label='Дата Закрытия',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=XDatepickerWidget)

    class Meta:
        model = Program
        fields = ['start_date', 'end_date', 'status', 'name', 'description', 'comment']

