import datetime

from django import forms
from django.contrib.admin import widgets


class DeviceForm(forms.ModelForm):
    wifi_signature = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 4}))
