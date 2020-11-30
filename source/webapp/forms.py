from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from .models import PROGRAM_STATUS_CHOICES, Program

default_status = PROGRAM_STATUS_CHOICES[0][0]


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['author', 'skills', 'child', 'is_deleted', 'deleted_date',]

