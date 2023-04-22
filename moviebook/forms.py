from django import forms
from .models import Film, Uzivatel, Tag

class FilmForm(forms.ModelForm):
    tagy = forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required = False)
    class Meta:
        model = Film
        fields=["nazev", "rezie", "zanr", "tagy"]


class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = Uzivatel
        fields = ["email", "password"]


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ["email", "password"]
