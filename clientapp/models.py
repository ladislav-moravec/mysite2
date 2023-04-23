from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Pojisteni(models.Model):
    nazev_pojisteni = models.CharField(max_length=80, verbose_name="Pojištění")

    def __str__(self):
        return "Nazev_pojisteni: {0}".format(self.nazev_pojisteni)

    class Meta:
        verbose_name = "Pojištění"
        verbose_name_plural = "Pojištění"


class Tag(models.Model):
    tag_title = models.CharField(max_length=30, verbose_name="Tagy")

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagy"


class Klient(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Jméno klienta")
    pojistovna = models.CharField(max_length=180, verbose_name="Pojišťovna")
    nazev_pojisteni = models.ForeignKey(Pojisteni, on_delete=models.SET_NULL, null=True, verbose_name="Pojištění")
    tagy = models.ManyToManyField(Tag)

    def __init__(self, *args, **kwargs):
        super(Klient, self).__init__(*args, **kwargs)

    def __str__(self):
        tags = [i.tag_title for i in self.tagy.all()]
        return "Jmeno klienta: {0} | Pojistovna: {1} | Pojisteni: {2} | Tagy: {3}".format(self.nazev, self.pojistovna, self.nazev_pojisteni,
                                                                             tags)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Filmy"


class UzivatelManager(BaseUserManager):
    # Vytvoří uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user

    # Vytvoří admina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user


class Uzivatel(AbstractBaseUser):
    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True