from django import forms
from .models import Klient, Uzivatel, Tag

class KlientForm(forms.ModelForm):
    tagy = forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required = False)
    class Meta:
        model = Klient
        fields=["klient", "pojistovna", "pojisteni", "tagy"]


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
