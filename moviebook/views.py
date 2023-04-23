from django.shortcuts import render
from django.views import generic

from .models import Film, Uzivatel
from .forms import FilmForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("filmovy_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("filmovy_index"))
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
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("filmovy_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("filmovy_index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))

class CreateFilm(LoginRequiredMixin, generic.edit.CreateView):

    form_class = FilmForm
    template_name = "moviebook/create_film.html"

# Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání filmu.")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

# Metoda pro POST request, zkontroluje formulář, pokud je validní vytvoří nový film, pokud ne zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání filmu.")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("filmovy_index")
        return render(request, self.template_name, {"form":form})


class CurrentFilmView(generic.DetailView):

    model = Film
    template_name = "moviebook/film_detail.html"

    def get(self, request, pk):
        try:
            film = self.get_object()
        except:
            return redirect("filmovy_index")
        return render(request, self.template_name, {"film" : film})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_film", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání filmu.")
                    return redirect(reverse("filmovy_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("filmovy_index"))



class EditFilm(LoginRequiredMixin, generic.edit.CreateView):
    form_class = FilmForm
    template_name = "moviebook/create_film.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu filmu.")
            return redirect(reverse("filmovy_index"))
        try:
            film = Film.objects.get(pk = pk)
        except:
            messages.error(request, "Tento film neexistuje!")
            return redirect("filmovy_index")
        form = self.form_class(instance=film)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu filmu.")
            return redirect(reverse("filmovy_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            nazev = form.cleaned_data["nazev"]
            rezie = form.cleaned_data["rezie"]
            zanr = form.cleaned_data["zanr"]
            tagy = form.cleaned_data["tagy"]
            try:
                film = Film.objects.get(pk = pk)
            except:
                messages.error(request, "Tento film neexistuje!")
                return redirect(reverse("filmovy_index"))
            film.nazev = nazev
            film.rezie = rezie
            film.zanr = zanr
            film.tagy.set(tagy)
            film.save()
        #return render(request, self.template_name, {"form":form})
        return redirect("filmovy_detail", pk = film.id)
