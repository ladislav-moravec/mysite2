from django.db import models

class Film(models.Model):
    nazev = models.CharField(max_length=200)
    rezie = models.CharField(max_length=180)

    def __str__(self):
        return "Nazev: {0} | Rezie: {1}".format(self.nazev, self.rezie)

class Zanr(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, default=1)
    nazev_zanru = models.CharField(max_length=80)

    def __str__(self):
        return "Film: {0} | Nazev_zanru: {1}".format(self.film, self.nazev_zanru)
