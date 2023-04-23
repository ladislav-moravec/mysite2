from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Zanr(models.Model):
    nazev_zanru = models.CharField(max_length=80, verbose_name="Žánr")

    def __str__(self):
        return "Nazev_zanru: {0}".format(self.nazev_zanru)

    class Meta:
        verbose_name = "Žánr"
        verbose_name_plural = "Žánry"


class Tag(models.Model):
    tag_title = models.CharField(max_length=30, verbose_name="Tagy")

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagy"


class Film(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Název Filmu")
    rezie = models.CharField(max_length=180, verbose_name="Režie")
    zanr = models.ForeignKey(Zanr, on_delete=models.SET_NULL, null=True, verbose_name="Žánr")
    tagy = models.ManyToManyField(Tag)

    def __init__(self, *args, **kwargs):
        super(Film, self).__init__(*args, **kwargs)

    def __str__(self):
        tags = [i.tag_title for i in self.tagy.all()]
        return "Nazev: {0} | Rezie: {1} | Zanr: {2} | Tagy: {3}".format(self.nazev, self.rezie, self.zanr.nazev_zanru,
                                                                        tags)

    class Meta:
        verbose_name = "Film"
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