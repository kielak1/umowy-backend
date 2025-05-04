from django.db import models
from django.contrib.auth.models import User
from authz.models import OrganizationalUnit


class Kontakt(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Kontrahent(models.Model):
    nazwa = models.CharField(max_length=255)
    kontakt = models.ForeignKey(Kontakt, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nazwa


class Umowa(models.Model):
    numer = models.CharField(max_length=100)  # Numer CRB
    kontrahent = models.ForeignKey(Kontrahent, on_delete=models.CASCADE)
    jednostka_organizacyjna = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, null=True)

    czy_ramowa = models.BooleanField(default=False)
    czy_dotyczy_konkretnych_uslug = models.BooleanField(default=True)

    czy_spelnia_dora = models.BooleanField(default=False)
    czy_wymaga_kontynuacji = models.BooleanField(default=False)
    wymagana_data_kontynuacji = models.DateField(null=True, blank=True)

    opiekun = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prowadzone_umowy')

    def __str__(self):
        return self.numer


class ZmianaUmowy(models.Model):
    RODZAJE = [
        ("umowa", "Umowa"),
        ("aneks", "Aneks"),
        ("porozumienie", "Porozumienie"),
        ("inne", "Inna zmiana"),
    ]

    WALUTY = [
        ("PLN", "Polski złoty"),
        ("EUR", "Euro"),
        ("USD", "Dolar amerykański"),
    ]

    umowa = models.ForeignKey(Umowa, on_delete=models.CASCADE, related_name="zmiany")
    rodzaj = models.CharField(max_length=20, choices=RODZAJE)

    przedmiot = models.CharField(max_length=500, null=True, blank=True)  # Nazwa
    producenci = models.TextField(null=True, blank=True)  # Długi tekst

    numer_umowy_dostawcy = models.CharField(max_length=100, null=True, blank=True)

    data_zawarcia = models.DateField()
    data_obowiazywania_od = models.DateField()
    data_obowiazywania_do = models.DateField(null=True, blank=True)

    kwota_netto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    waluta = models.CharField(max_length=10, choices=WALUTY, default="PLN")
    opis = models.TextField(blank=True)  # Informacje o umowie

    # ➕ NOWE POLA:
    kategoria = models.ForeignKey("SlownikKategoriaUmowy", on_delete=models.SET_NULL, null=True, blank=True)
    obszary_funkcjonalne = models.ManyToManyField("SlownikObszarFunkcjonalny", blank=True)
    wlasciciel = models.ForeignKey("SlownikWlasciciel", on_delete=models.SET_NULL, null=True, blank=True)
    data_podpisania = models.DateField(null=True, blank=True)
    data_wypowiedzenia = models.DateField(null=True, blank=True)
    trzeba_wypowiedziec = models.BooleanField(default=False)
    status = models.ForeignKey("SlownikStatusUmowy", on_delete=models.SET_NULL, null=True, blank=True)
    finansowanie_do = models.DateField(null=True, blank=True)
    klasyfikacja = models.ForeignKey("SlownikKlasyfikacjaUmowy", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.rodzaj} ({self.data_zawarcia})"


class Zamowienie(models.Model):
    WALUTY = [
        ("PLN", "Polski złoty"),
        ("EUR", "Euro"),
        ("USD", "Dolar amerykański"),
    ]

    umowa = models.ForeignKey(Umowa, on_delete=models.CASCADE, related_name="zamowienia")
    przedmiot = models.CharField(max_length=500, null=True, blank=True)
    producenci = models.CharField(max_length=500, null=True, blank=True)
    numer_zamowienia = models.CharField(max_length=100)
    data_zlozenia = models.DateField()
    data_realizacji = models.DateField(null=True, blank=True)

    kwota_netto = models.DecimalField(max_digits=12, decimal_places=2)
    waluta = models.CharField(max_length=10, choices=WALUTY, default="PLN")
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.numer_zamowienia


# Tabele słownikowe (na początek jako proste modele – można rozwinąć np. o slug)
class SlownikKategoriaUmowy(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa


class SlownikObszarFunkcjonalny(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa


class SlownikWlasciciel(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class SlownikStatusUmowy(models.Model):
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwa


class SlownikKlasyfikacjaUmowy(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa
