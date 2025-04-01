from django import forms
from tinymce.widgets import TinyMCE

from .models import Advert, Respond


class AdvertForm(forms.ModelForm):

    class Meta:
        model = Advert
        fields = ['category', 'header', 'content']
        widgets = {'content': TinyMCE()}


class RespondForm(forms.ModelForm):
    class Meta:
        model = Respond
        fields = ['content']
