from django import forms
from .models import Film

class FilmForm(forms.ModelForm):

    class Meta:
        model = Film
        fields=["nazev", "rezie", "zanr"]
