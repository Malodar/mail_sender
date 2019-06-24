# -*- coding: UTF-8 -*-
from django import forms
from .models import Event
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class EventUploadFileForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['file_csv', 'day', 'time']
        widgets = {
            'day': DatePickerInput(),
            'time': TimePickerInput(),
        }
