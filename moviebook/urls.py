from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("film_index/", views.FilmIndex.as_view(), name="filmovy_index"),
    path("<int:pk>/film_detail/", views.CurrentFilmView.as_view(), name="filmovy_detail"),
    path("create_film/", views.CreateFilm.as_view(), name="novy_film"),
]