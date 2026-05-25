# Modul opisujacy swiat symulacji - mape, granice, elementy.

import math
import random


# Stale uzywane w roznych miejscach programu.
# Trzymam je tutaj zeby latwo bylo cos zmienic w jednym miejscu.
ENERGIA_NA_RUCH = 5       # ile energii kosztuje jeden ruch do przodu
DLUGOSC_KROKU = 5          # o ile jednostek lazik przesuwa sie w jednym ruchu
PROMIEN_INTERAKCJI = 4     # w jakim zasiegu lazik "wchodzi" w element

# Kolory dla turtle dla kazdego typu elementu.
KOLORY_ELEMENTOW = {
    "krater": "saddlebrown",
    "kamien": "gray",
    "panel": "gold",
    "probka": "deepskyblue",
    "stacja": "red",
}


class Swiat:
    # rozmiar mapy i lista elementow

    def __init__(self, rozmiar):
        # mapa jest kwadratowa od -rozmiar do +rozmiar
        self.rozmiar = rozmiar
        self.elementy = []   # lista slownikow {x, y, typ, wartosc, uzyty}

    def dodaj_element(self, x, y, typ, wartosc=0):
        self.elementy.append({
            "x": x,
            "y": y,
            "typ": typ,
            "wartosc": wartosc,
            "uzyty": False,
        })

    def w_granicach(self, x, y):
        return (-self.rozmiar <= x <= self.rozmiar
                and -self.rozmiar <= y <= self.rozmiar)

    def znajdz_element_w_poblizu(self, x, y):
        #Zwraca pierwszy element w promieniu PROMIEN_INTERAKCJI,ktory jeszcze nie zostal uzyty. Jak nic nie ma to zwraca None.Kratery sa wyjatkiem - nigdy nie znikaja."""

        for e in self.elementy:
            if e["uzyty"] and e["typ"] != "krater":
                continue
            odleglosc = math.sqrt((e["x"] - x) ** 2 + (e["y"] - y) ** 2)
            if odleglosc <= PROMIEN_INTERAKCJI:
                return e
        return None


def wygeneruj_swiat(rozmiar, trudnosc):
    #Tworzy nowy swiat z losowymi elementami.Trudnosc 1-3 wplywa na liczbe kraterow i paneli.
    swiat = Swiat(rozmiar)

    # liczba elementow zalezna od rozmiaru i trudnosci
    liczba_kraterow = 4 + trudnosc * 2 + rozmiar // 20
    liczba_kamieni = 5 + rozmiar // 25
    liczba_paneli = max(2, 5 - trudnosc)
    liczba_probek = 4 + rozmiar // 30

    # Kratery - przeszkody, blokuja ruch i zabieraja energie
    for _ in range(liczba_kraterow):
        x = random.randint(-rozmiar + 10, rozmiar - 10)
        y = random.randint(-rozmiar + 10, rozmiar - 10)
        # nie chcemy kratera obok pozycji startowej (0,0)
        if abs(x) < 15 and abs(y) < 15:
            continue
        swiat.dodaj_element(x, y, "krater", wartosc=10)

    # Kamienie - utrudniaja ruch (lazik traci wiecej energii)
    for _ in range(liczba_kamieni):
        x = random.randint(-rozmiar + 5, rozmiar - 5)
        y = random.randint(-rozmiar + 5, rozmiar - 5)
        swiat.dodaj_element(x, y, "kamien", wartosc=5)

    # Panele sloneczne - bonus energii
    for _ in range(liczba_paneli):
        x = random.randint(-rozmiar + 5, rozmiar - 5)
        y = random.randint(-rozmiar + 5, rozmiar - 5)
        swiat.dodaj_element(x, y, "panel", wartosc=25)

    # Probki - punkty za zebranie
    for _ in range(liczba_probek):
        x = random.randint(-rozmiar + 5, rozmiar - 5)
        y = random.randint(-rozmiar + 5, rozmiar - 5)
        swiat.dodaj_element(x, y, "probka", wartosc=10)

    # Stacja meteorologiczna - cel wyprawy, jedna sztuka, gdzies daleko
    while True:
        sx = random.randint(-rozmiar + 10, rozmiar - 10)
        sy = random.randint(-rozmiar + 10, rozmiar - 10)
        if math.sqrt(sx * sx + sy * sy) > rozmiar * 0.5:
            break
    swiat.dodaj_element(sx, sy, "stacja", wartosc=100)

    return swiat


def znajdz_cel(swiat):
    #Zwraca (x, y) stacji meteorologicznej - zaklada ze jest dokladnie jedna.
    for e in swiat.elementy:
        if e["typ"] == "stacja":
            return e["x"], e["y"]
    return 0, 0
