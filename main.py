# Symulator misji lazika marsjanskiego
# Gigathon 2026 - III etap, Python 16-18 lat
#
# Plik glowny - obsluguje wejscie od uzytkownika, glowna petle symulacji
# i ponowne uruchamianie wyprawy. Logika jest podzielona na osobne moduly:
#   swiat.py        - mapa i elementy
#   lazik.py        - klasa lazika i akcje
#   zdarzenia.py    - losowe zdarzenia
#   wizualizacja.py - rysowanie trasy w turtle
#   raport.py       - naglowek, pomoc, raport koncowy

import math
import os

from swiat import wygeneruj_swiat, znajdz_cel, PROMIEN_INTERAKCJI
from lazik import Lazik, ruch_do_przodu, skret, odpoczynek, skanowanie
from zdarzenia import sprobuj_zdarzenie_losowe
from wizualizacja import narysuj_trase
from raport import wypisz_naglowek, wypisz_pomoc_akcji, wypisz_raport

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
BLUE = "\033[38;5;75m"
GREEN = "\033[92m"
YELLOW = "\033[38;5;180m"
RED = "\033[91m"
MAGENTA = "\033[38;5;146m"
WHITE = "\033[38;5;252m"
GRAY = "\033[38;5;245m"


def koloruj(tekst, kolor, pogrub=False):
    start = kolor
    if pogrub:
        start += BOLD
    return f"{start}{tekst}{RESET}"


def wyczysc_ekran():
    os.system("cls")


def wybierz_kolor_linii(linia):
    tekst = linia.lower()
    if ("dotarl" in tekst or "zebrano probke" in tekst or "panelu slonecznego" in tekst
            or "energia +" in tekst or "zapasowy ogniwo" in tekst or "odpoczynek" in tekst
            or "wygrywasz" in tekst):
        return GREEN
    if ("burza" in tekst or "krater" in tekst or "stracono" in tekst
            or "wyczerpanie" in tekst or "porazka" in tekst
            or "(-" in tekst or "nieznana akcja" in tekst):
        return RED
    if "skan okolic" in tekst or "krok " in tekst or "wybierz akcje" in tekst:
        return CYAN
    if "zdarzenie" in tekst:
        return YELLOW
    return WHITE


def wypisz_kolorowo(tekst, pogrub=False):
    for linia in tekst.splitlines():
        print(koloruj(linia, wybierz_kolor_linii(linia), pogrub))


def pokaz_menu_startowe():
    while True:
        wyczysc_ekran()
        print(koloruj("=" * 64, BLUE, True))
        print(koloruj("        SYMULATOR MISJI LAZIKA MARSJANSKIEGO", CYAN, True))
        print(koloruj("=" * 64, BLUE, True))
        print(koloruj("  [1] Rozpocznij gre", WHITE, True))
        print(koloruj("  [2] Zasady", WHITE, True))
        print(koloruj("  [3] Wyjscie", WHITE, True))
        print(koloruj("=" * 64, BLUE, True))
        wybor = input(koloruj("Wybierz opcje: ", CYAN, True)).strip()

        if wybor == "1":
            return "gra"
        if wybor == "2":
            pokaz_zasady()
            continue
        if wybor == "3":
            return "wyjscie"

        print(koloruj("Niepoprawny wybor. Wpisz 1, 2 albo 3.", RED, True))


def pokaz_zasady():
    print()
    print(koloruj("=" * 64, BLUE, True))
    print(koloruj("ZASADY MISJI", CYAN, True))
    print(koloruj("=" * 64, BLUE, True))
    print(koloruj("Mozliwe zdarzenia:", YELLOW, True))
    print(koloruj("  Burza pylowa zabiera od 6 do 12 energii.", WHITE))
    print(koloruj("  Zapasowe ogniwo dodaje od 8 do 15 energii.", WHITE))
    print(koloruj("  Usterka napedu moze obrocic lazik o 30 lub 45 stopni.", WHITE))
    print(koloruj("  Silny wiatr moze przesunac lazik na osi X albo Y.", WHITE))
    print()
    print(koloruj("Przedmioty i elementy mapy:", YELLOW, True))
    print(koloruj("  Krater zatrzymuje lazik i odbiera dodatkowe 10 energii.", WHITE))
    print(koloruj("  Kamieniste pole zwieksza koszt ruchu o 5 energii.", WHITE))
    print(koloruj("  Panel sloneczny daje 25 energii.", WHITE))
    print(koloruj("  Probka skaly daje punkty po zebraniu.", WHITE))
    print(koloruj("  Stacja meteorologiczna jest celem wyprawy.", WHITE))
    print()
    print(koloruj("Kiedy wygrywasz:", YELLOW, True))
    print(koloruj("  Wygrywasz, gdy dotrzesz do stacji meteorologicznej.", GREEN, True))
    print(koloruj("  Przegrywasz, gdy energia spadnie do zera.", RED))
    print(koloruj("  Przegrywasz, gdy przekroczysz limit krokow.", RED))
    print(koloruj("  Mozesz tez przerwac misje klawiszem q.", MAGENTA))
    print()
    print(koloruj("Sterowanie w grze:", YELLOW, True))
    print(koloruj("  w - ruch do przodu", WHITE))
    print(koloruj("  a - skret w lewo", WHITE))
    print(koloruj("  d - skret w prawo", WHITE))
    print(koloruj("  s - odpoczynek", WHITE))
    print(koloruj("  k - skanowanie", WHITE))
    print(koloruj("  h - pomoc", WHITE))
    print(koloruj("  q - koniec misji", WHITE))
    print(koloruj("=" * 64, BLUE, True))
    input(koloruj("Nacisnij Enter, aby wrocic do menu... ", CYAN, True))
    wyczysc_ekran()



# POMOCNICZE FUNKCJE WEJSCIA


def zapytaj_o_liczbe(tekst, minimum, maximum, wartosc_domyslna):
    # funkcja pyta o liczbe całkowita uzytkownika (max 3 raz)
    proby = 0
    while proby < 3:
        odp = input(tekst).strip()
        if odp == "":
            print(koloruj(f"  -> przyjmuje wartosc domyslna: {wartosc_domyslna}", GRAY))
            return wartosc_domyslna
        try:
            wartosc = int(odp)
        except ValueError:
            print(koloruj("  ! to nie jest liczba calkowita, sprobuj jeszcze raz", RED, True))
            proby += 1
            continue
        if wartosc < minimum or wartosc > maximum:
            print(koloruj(f"  ! liczba musi byc miedzy {minimum} a {maximum}", RED, True))
            proby += 1
            continue
        return wartosc
    print(koloruj(f"  -> za duzo blednych prob, biore wartosc domyslna: {wartosc_domyslna}", GRAY))
    return wartosc_domyslna


def zapytaj_o_tekst(tekst, wartosc_domyslna):
    odp = input(tekst).strip()
    if odp == "":
        return wartosc_domyslna
    return odp


# GLOWNA PETLA SYMULACJI


def uruchom_symulacje(lazik, swiat, cel_x, cel_y, limit_krokow):
    #Glowna petla

    powod_konca = ""
    wynik = ""

    wypisz_pomoc_akcji()

    while True:
        # sprawdzenie warunkow konca PRZED nowym krokiem
        if lazik.energia <= 0:
            powod_konca = "calkowite wyczerpanie energii"
            wynik = "PORAZKA"
            break
        if lazik.kroki >= limit_krokow:
            powod_konca = "przekroczono limit krokow"
            wynik = "PORAZKA"
            break

        lazik.kroki += 1
        print()
        print(koloruj("-" * 60, BLUE))
        print(koloruj(
            f"KROK {lazik.kroki}/{limit_krokow}  |  pozycja=({lazik.x}, {lazik.y})  |  kat={lazik.kat}  |  energia={lazik.energia}",
            CYAN, True))
        print(koloruj("-" * 60, BLUE))

        akcja = input(koloruj("Wybierz akcje [w/a/d/s/k/q] (h = pomoc): ", CYAN, True)).strip().lower()

        if akcja == "":
            # pusta akcja
            akcja = "w"

        if akcja == "h":
            wypisz_pomoc_akcji()
            lazik.kroki -= 1  # to nie byl prawdziwy krok
            continue

        opis_akcji = ""

        if akcja == "w":
            opis_akcji = ruch_do_przodu(lazik, swiat)
        elif akcja == "a":
            opis_akcji = skret(lazik, w_lewo=True)
        elif akcja == "d":
            opis_akcji = skret(lazik, w_lewo=False)
        elif akcja == "s":
            opis_akcji = odpoczynek(lazik)
        elif akcja == "k":
            opis_akcji = skanowanie(lazik, swiat)
        elif akcja == "q":
            powod_konca = "uzytkownik zakonczyl wyprawe wczesniej"
            wynik = "PRZERWANIE"
            break
        else:
            print("  ! nieznana akcja, sprobuj jeszcze raz")
            lazik.kroki -= 1
            continue

        wypisz_kolorowo(opis_akcji)
        lazik.dodaj_log(f"krok {lazik.kroki}: akcja '{akcja}' - {opis_akcji.strip()}")

        #sprawdzenie czy dotarl do celu
        d_cel = math.sqrt((lazik.x - cel_x) ** 2 + (lazik.y - cel_y) ** 2)
        if d_cel <= PROMIEN_INTERAKCJI:
            print()
            print(koloruj(f"  *** LAZIK DOTARL DO STACJI METEOROLOGICZNEJ NA ({cel_x}, {cel_y})!", GREEN, True))
            powod_konca = "dotarcie do stacji meteorologicznej"
            wynik = "SUKCES"
            break

        # losowe zdarzenie
        if akcja in ("w", "a", "d"):
            zdarz = sprobuj_zdarzenie_losowe(lazik)
            if zdarz:
                wypisz_kolorowo(zdarz, True)
                lazik.dodaj_log(f"krok {lazik.kroki}: {zdarz.strip()}")

        # jeszcze raz sprawdzamy energie
        if lazik.energia <= 0:
            powod_konca = "calkowite wyczerpanie energii po zdarzeniu losowym"
            wynik = "PORAZKA"
            break

    return wynik, powod_konca



# CALY JEDEN PRZEBIEG GRY


def rozegraj_jedna_wyprawe():
    wyczysc_ekran()
    print()
    print(koloruj("###  SYMULATOR MISJI LAZIKA MARSJANSKIEGO  ###", CYAN, True))
    print()
    print(koloruj("Najpierw podaj kilka parametrow wyprawy.", WHITE))
    print(koloruj("Mozesz pominac kazde pytanie naciskajac Enter - wtedy bedzie wartosc domyslna.", WHITE))
    print()

    nazwa = zapytaj_o_tekst(koloruj("Nazwa lazika (np. 'Curiosity'): ", CYAN, True), "Lazik-1")

    rozmiar = zapytaj_o_liczbe(
        koloruj("Rozmiar mapy (50-200, domyslnie 100): ", CYAN, True), 50, 200, 100)

    x = zapytaj_o_liczbe(
        koloruj(f"Pozycja startowa X (od -{rozmiar} do {rozmiar}, domyslnie 0): ", CYAN, True),
        -rozmiar, rozmiar, 0)
    y = zapytaj_o_liczbe(
        koloruj(f"Pozycja startowa Y (od -{rozmiar} do {rozmiar}, domyslnie 0): ", CYAN, True),
        -rozmiar, rozmiar, 0)
    kat = zapytaj_o_liczbe(
        koloruj("Kat startowy (0-359, domyslnie 0 = wschod): ", CYAN, True), 0, 359, 0)
    energia = zapytaj_o_liczbe(
        koloruj("Energia startowa (50-300, domyslnie 150): ", CYAN, True), 50, 300, 150)
    trudnosc = zapytaj_o_liczbe(
        koloruj("Poziom trudnosci (1 = latwy, 2 = sredni, 3 = trudny; domyslnie 2): ", CYAN, True),
        1, 3, 2)

    # limit krokow zalezny od rozmiaru mapy
    limit_krokow = rozmiar + 50

    swiat = wygeneruj_swiat(rozmiar, trudnosc)
    lazik = Lazik(nazwa, x, y, kat, energia)
    cel_x, cel_y = znajdz_cel(swiat)

    wypisz_naglowek(lazik, swiat, cel_x, cel_y, limit_krokow)

    wynik, powod = uruchom_symulacje(lazik, swiat, cel_x, cel_y, limit_krokow)

    wypisz_raport(lazik, swiat, cel_x, cel_y, limit_krokow, wynik, powod)

    # turtle
    try:
        narysuj_trase(lazik, swiat, cel_x, cel_y,
                      f"Misja: {lazik.nazwa} ({wynik})")
    except Exception as exc:
        # gdyby cos sie zepsulo z turtle (np. brak srodowiska graficznego)
        print(f"  (nie udalo sie otworzyc okna turtle: {exc})")
    input(koloruj("Nacisnij Enter, aby wrocic do menu... ", CYAN, True))
    wyczysc_ekran()


def main():
    while True:
        wybor_menu = pokaz_menu_startowe()
        if wybor_menu == "wyjscie":
            wyczysc_ekran()
            print(koloruj("Dziekuje za korzystanie z symulatora. Do zobaczenia!", CYAN, True))
            break

        rozegraj_jedna_wyprawe()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Program przerwany przez uzytkownika (Ctrl+C). Pa!")
