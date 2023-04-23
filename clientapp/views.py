from django.shortcuts import render
from django.views import generic

from .models import Klient, Uzivatel
from .forms import KlientForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class FilmIndex(generic.ListView):
    template_name = "clientapp/klient_index.html"  # cesta k templatu ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "filmy"  # pod tímto jménem budeme volat list objektů v templatu

    # tato funkce nám získává list klientů od největšího id (9,8,7...)
    def get_queryset(self):
        return Klient.objects.all().order_by("-id")


class CurrentFilmView(generic.DetailView):
    model = Klient
    template_name = "clientapp/klient_detail.html"


class CreateFilm(generic.edit.CreateView):
    form_class = KlientForm
    template_name = "clientapp/create_klient.html"

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    # Metoda pro POST request, zkontroluje formulář, pokud je validní vytvoří nový klient, pokud ne zobrazí formulář s chybovou hláškou
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "clientapp/user_form.html"

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
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit = False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("klient_index")

        return render(request, self.template_name, {"form":form})


class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "clientapp/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("klient_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("klient_index")
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

    form_class = KlientForm
    template_name = "clientapp/create_klient.html"

# Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

# Metoda pro POST request, zkontroluje formulář, pokud je validní vytvoří nový film, pokud ne zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("klient_index")
        return render(request, self.template_name, {"form":form})


class CurrentFilmView(generic.DetailView):

    model = Klient
    template_name = "clientapp/klient_detail.html"

    def get(self, request, pk):
        try:
            film = self.get_object()
        except:
            return redirect("klient_index")
        return render(request, self.template_name, {"klient" : klient})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_klient", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání klienta.")
                    return redirect(reverse("klient_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("klient_index"))



class EditFilm(LoginRequiredMixin, generic.edit.CreateView):
    form_class = KlientForm
    template_name = "clientapp/create_klient.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu klienta.")
            return redirect(reverse("klient_index"))
        try:
            film = Klient.objects.get(pk = pk)
        except:
            messages.error(request, "Tento klient neexistuje!")
            return redirect("klient_index")
        form = self.form_class(instance=film)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            nazev = form.cleaned_data["nazev"]
            rezie = form.cleaned_data["pojistovna"]
            zanr = form.cleaned_data["pojisteni"]
            tagy = form.cleaned_data["tagy"]
            try:
                klient = Klient.objects.get(pk = pk)
            except:
                messages.error(request, "Tento klient neexistuje!")
                return redirect(reverse("klient_index"))
            klient.nazev = nazev
            klient.pojistovna = rezie
            klient.pojisteni = zanr
            klient.tagy.set(tagy)
            klient.save()
        #return render(request, self.template_name, {"form":form})
        return redirect("klient_detail", pk = klient.id)
