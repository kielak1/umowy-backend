from django.contrib import admin
from .models import Kontakt, Kontrahent, Umowa, ZmianaUmowy, Zamowienie

@admin.register(Kontakt)
class KontaktAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'email', 'telefon')
    search_fields = ('imie', 'nazwisko', 'email')


@admin.register(Kontrahent)
class KontrahentAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kontakt')
    search_fields = ('nazwa',)


@admin.register(Umowa)
class UmowaAdmin(admin.ModelAdmin):
    list_display = (
        'numer',
        'czy_ramowa',
        'czy_dotyczy_konkretnych_uslug',
        'czy_wymaga_kontynuacji',
        'czy_spelnia_dora',
        'kontrahent',
    )
    list_filter = (
        'czy_ramowa',
        'czy_dotyczy_konkretnych_uslug',
        'czy_wymaga_kontynuacji',
        'czy_spelnia_dora',
    )
    search_fields = ('numer',)

@admin.register(ZmianaUmowy)
class ZmianaUmowyAdmin(admin.ModelAdmin):
    list_display = ('umowa', 'rodzaj', 'data_zawarcia', 'kwota_netto', 'waluta')
    search_fields = ('umowa__numer',)
    list_filter = ('rodzaj', 'waluta')


@admin.register(Zamowienie)
class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ('umowa', 'numer_zamowienia', 'data_zlozenia', 'kwota_netto', 'waluta')
    search_fields = ('numer_zamowienia', 'umowa__numer')
    list_filter = ('waluta',)
