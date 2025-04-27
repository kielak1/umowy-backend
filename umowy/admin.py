from django.contrib import admin
from django.contrib import admin
from .models import Kontakt, Kontrahent, Umowa

@admin.register(Kontakt)
class KontaktAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'email', 'telefon')
    search_fields = ('imie', 'nazwisko', 'email')

@admin.register(Kontrahent)
class KontrahentAdmin(admin.ModelAdmin):
    list_display = ('nazwa_kontrahenta', 'kontakt')
    search_fields = ('nazwa_kontrahenta',)

@admin.register(Umowa)
class UmowaAdmin(admin.ModelAdmin):
    list_display = ('numer', 'przedmiot', 'data_zawarcia', 'czy_wymaga_kontynuacji', 'czy_spelnia_wymagania_dora', 'kontrahent')
    list_filter = ('czy_wymaga_kontynuacji', 'czy_spelnia_wymagania_dora')
    search_fields = ('numer', 'przedmiot')
