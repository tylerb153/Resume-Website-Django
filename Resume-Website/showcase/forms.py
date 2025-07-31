from django import forms
from .models import Build

class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ['title', 'creator', 'coordsx', 'coordsy', 'coordsz', 'description']