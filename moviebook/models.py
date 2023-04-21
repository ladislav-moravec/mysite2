from django.db import models
#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class Zanr(models.Model):
    nazev_zanru = models.CharField(max_length=80, verbose_name="Žánr")

    def __str__(self):
        return "Nazev_zanru: {0}".format(self.nazev_zanru)

    class Meta:
        verbose_name="Žánr"
        verbose_name_plural="Žánry"

class Film(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Název Filmu")
    rezie = models.CharField(max_length=180, verbose_name="Režie")
    zanr = models.ForeignKey(Zanr, on_delete=models.SET_NULL, null=True, verbose_name="Žánr")

    def __str__(self):
        return "Nazev: {0} | Rezie: {1} | Zanr: {2}".format(self.nazev, self.rezie, self.zanr.nazev_zanru)

    class Meta:
        verbose_name="Film"
        verbose_name_plural="Filmy"