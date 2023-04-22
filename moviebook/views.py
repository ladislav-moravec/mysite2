from django.shortcuts import render
from django.views import generic

from .models import Film, Uzivatel
from .forms import FilmForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse

from django.contrib import messages



class FilmIndex(generic.ListView):
    template_name = "moviebook/film_index.html"  # cesta k templatu ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "filmy"  # pod tímto jménem budeme volat list objektů v templatu

    # tato funkce nám získává list filmů od největšího id (9,8,7...)
    def get_queryset(self):
        return Film.objects.all().order_by("-id")


class CurrentFilmView(generic.DetailView):
    model = Film
    template_name = "moviebook/film_detail.html"


class CreateFilm(generic.edit.CreateView):
    form_class = FilmForm
    template_name = "moviebook/create_film.html"

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    # Metoda pro POST request, zkontroluje formulář, pokud je validní vytvoří nový film, pokud ne zobrazí formulář s chybovou hláškou
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "moviebook/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit = False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("filmovy_index")

        return render(request, self.template_name, {"form":form})


class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "moviebook/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("filmovy_index")
        return render(request, self.template_name, {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))
