from django.urls import path
from . import views
from . import url_handlers

urlpatterns = [
    #path("", views.index, name="index"),
    path("klient_index/", views.FilmIndex.as_view(), name="klient_index"),
    path("<int:pk>/klient_detail/", views.CurrentFilmView.as_view(), name="klient_detail"),
    path("create_klient/", views.CreateFilm.as_view(), name="novy_klient"),
    path("", url_handlers.index_handler),
    path("register/", views.UzivatelViewRegister.as_view(), name = "registrace"),
    path("login/", views.UzivatelViewLogin.as_view(), name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("<int:pk>/edit/", views.EditFilm.as_view(), name="edit_klient"),
]