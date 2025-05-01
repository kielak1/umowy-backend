from django.db import models
from django.contrib.auth.models import User
from authz.models import OrganizationalUnit  # import z authz

class Kontakt(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Kontrahent(models.Model):
    nazwa_kontrahenta = models.CharField(max_length=255)
    kontakt = models.ForeignKey(Kontakt, on_delete=models.CASCADE, related_name='kontrahenci')

    def __str__(self):
        return self.nazwa_kontrahenta

class Umowa(models.Model):
    numer = models.CharField(max_length=100)
    przedmiot = models.TextField()
    data_zawarcia = models.DateField()
    czy_wymaga_kontynuacji = models.BooleanField(default=False)
    wymagana_data_zawarcia_kolejnej_umowy = models.DateField(null=True, blank=True)
    czy_spelnia_wymagania_dora = models.BooleanField(default=False)
    kontrahent = models.ForeignKey(Kontrahent, on_delete=models.CASCADE, related_name='umowy')

    opiekun = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prowadzone_umowy')
    org_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name='umowy')

    def __str__(self):
        return self.numer
