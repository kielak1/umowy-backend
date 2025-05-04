from django.contrib import admin
from .models import (
    Kontakt,
    Kontrahent,
    Umowa,
    ZmianaUmowy,
    Zamowienie,
    SlownikKategoriaUmowy,
    SlownikObszarFunkcjonalny,
    SlownikWlasciciel,
    SlownikStatusUmowy,
    SlownikKlasyfikacjaUmowy,
)


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
    list_display = (
        'umowa',
        'rodzaj',
        'data_zawarcia',
        'kwota_netto',
        'waluta',
        'kategoria',
        'status',
        'wlasciciel',
        'klasyfikacja',
        'wyswietl_obszary',
    )
    search_fields = ('umowa__numer', 'przedmiot', 'numer_umowy_dostawcy')
    list_filter = ('rodzaj', 'waluta', 'kategoria', 'status', 'wlasciciel', 'klasyfikacja')
    filter_horizontal = ('obszary_funkcjonalne',)

    def wyswietl_obszary(self, obj):
        return ", ".join([o.nazwa for o in obj.obszary_funkcjonalne.all()])
    wyswietl_obszary.short_description = "Obszary funkcjonalne"



@admin.register(Zamowienie)
class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ('umowa', 'numer_zamowienia', 'data_zlozenia', 'kwota_netto', 'waluta')
    search_fields = ('numer_zamowienia', 'umowa__numer')
    list_filter = ('waluta',)


# Rejestracja słowników
@admin.register(SlownikKategoriaUmowy)
class SlownikKategoriaUmowyAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


@admin.register(SlownikObszarFunkcjonalny)
class SlownikObszarFunkcjonalnyAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


@admin.register(SlownikWlasciciel)
class SlownikWlascicielAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


@admin.register(SlownikStatusUmowy)
class SlownikStatusUmowyAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


@admin.register(SlownikKlasyfikacjaUmowy)
class SlownikKlasyfikacjaUmowyAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)
