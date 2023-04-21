from django.shortcuts import render
from django.views import generic

from .models import Film
from .forms import FilmForm  # Nový import


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