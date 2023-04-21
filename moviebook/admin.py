from django.contrib import admin
from .models import Film, Zanr #Importujeme si modely

#Modely registrujeme
admin.site.register(Film)
admin.site.register(Zanr)
