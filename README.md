# Mapa Cen Paliw dla Miasta Poznania

## 1. Opis projektu

"Mapa cen paliw dla miasta Poznania" to aplikacja internetowa stworzona w celu umożliwenia użytkownikom lokalizacji oraz porównania cen paliw (PB95, PB98, Diesel, LPG) na stacjach paliw w granicach miasta. Główne funkcje to:

* Sortowanie stacji wg ceny paliwa
* Wyznaczanie najbliższych stacji na podstawie lokalizacji użytkownika
* Pomiar odległości użytkownika od stacji
* Crowdsourcingowa aktualizacja cen paliw

## 2. Technologie

* **Dash** (Python)
* **Dash Leaflet** (interaktywna mapa)
* **Dash Bootstrap Components** (interfejs)
* **PostgreSQL + PostGIS** (baza danych przestrzennych)
* **psycopg2** (komunikacja z bazą danych)

## 3. Struktura aplikacji

### 3.1 Mapa cen paliw

Główna zakładka aplikacji zawiera:

* Interaktywną mapę z markerami stacji paliw i popupami z cenami
* Warstwy mapowe: OpenStreetMap, OpenTopoMap
* Granice dzielnic (GeoJSON)
* Komponenty dodatkowe: LocateControl, MeasureControl, EasyButton
* Formularz do aktualizacji cen z listą stacji, wyborem paliwa i polem ceny

### 3.2 Tabela cen paliw

Druga zakładka zawiera:

* Tabelę z nazwą stacji, cenami, dzielnicą i adresem
* Sortowanie wg wybranego paliwa
* Eksport do CSV

## 4. Baza danych

Główna tabela: `public.stacje_paliw`

Atrybuty:

* `nazwa_stacji`
* `adres`
* `dzielnica`
* `lat`, `lon`
* `diesel`, `lpg`, `pb95`, `pb98`

## 5. Backend i logika

* Połączenie z PostgreSQL przez `psycopg2`
* Callbacki realizujące aktualizację i pobieranie danych
* Przechowywanie części danych w komponencie `dcc.Store`

### Mechanizm aktualizacji cen:

1. Wybór stacji, typu paliwa, podanie ceny
2. Callback waliduje dane, wykonuje `UPDATE` w bazie, zwraca komunikat i odświeża mapę

## 6. Komponenty mapowe

* `dl.Map` z warstwami:

  * BaseLayer: podkłady kartograficzne
  * Overlay:

    * Markery stacji paliw (z popupem, nazwą, adresem, cenami)
    * Granice dzielnic (GeoJSON)

* `dl.LocateControl`: lokalizacja użytkownika

* `dl.MeasureControl`: pomiar odległości

* `dl.EasyButton`: reset widoku

## 7. Funkcjonalności techniczne

* Rozpoznawanie nazw stacji i przypisywanie logotypów do markerów
* Aktualizacja popupu po zmianie ceny

## 8. Status rozwoju

Aktualna wersja obsługuje operacje typu **Read** i **Update**. W przyszłości możliwa implementacja automatycznego pobierania danych ze stron stacji paliw.
