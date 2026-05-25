# Klasa Lazika i wszystkie akcje, ktore moze wykonac.

import math

from swiat import DLUGOSC_KROKU, ENERGIA_NA_RUCH


class Lazik:
    # stan lazika

    def __init__(self, nazwa, x, y, kat, energia):
        self.nazwa = nazwa
        self.x = x
        self.y = y
        self.kat = kat % 360          # kierunek w stopniach (0 = wschod)
        self.energia = energia

        # zachowujemy startowe wartosci do raportu na koncu
        self.energia_start = energia
        self.x_start = x
        self.y_start = y
        self.kat_start = kat

        # statystyki przebiegu wyprawy
        self.kroki = 0
        self.zebrane_probki = 0
        self.zaliczone_panele = 0
        self.uderzenia_w_krater = 0
        self.dziennik = []            # lista wpisow tekstowych
        self.trasa = [(x, y)]         # do rysowania w turtle

    def dodaj_log(self, tekst):
        self.dziennik.append(tekst)


def ruch_do_przodu(lazik, swiat):
    #przesuwa lazik o DLUGOSC_KROKU w aktualnym kierunku (zapisuje opis co się stało, żeby później można było wyświetlić w terminalu)
    stara_x = lazik.x
    stara_y = lazik.y
    stara_energia = lazik.energia

    # obliczenie nowej pozycji
    rad = math.radians(lazik.kat)
    nowa_x = round(lazik.x + DLUGOSC_KROKU * math.cos(rad), 1)
    nowa_y = round(lazik.y + DLUGOSC_KROKU * math.sin(rad), 1)

    # sprawdzamy granice swiata
    if not swiat.w_granicach(nowa_x, nowa_y):
        # zostajemy w miejscu, ale tracimy troche energii na "stuk w sciane"
        lazik.energia -= 2
        opis = (f"  Lazik probowal wyjsc poza mape. Zostal w miejscu. "
                f"(pozycja {stara_x}, {stara_y}) "
                f"-> energia: {stara_energia} => {lazik.energia} (-2)")
        return opis

    # mozemy sie ruszyc, zuzywamy energie
    koszt = ENERGIA_NA_RUCH
    powod_dodatkowy = ""

    # sprawdzamy czy w nowej pozycji jest jakis element
    element = swiat.znajdz_element_w_poblizu(nowa_x, nowa_y)
    if element is not None:
        if element["typ"] == "krater":
            # uderzenie w krater - zatrzymuje sie i traci energie
            koszt += element["wartosc"]
            powod_dodatkowy = " (wpadl do krateru -10 energii ekstra)"
            lazik.uderzenia_w_krater += 1
            # lazik nie wlatuje do krateru, zatrzymuje sie tuz obok
            nowa_x = stara_x
            nowa_y = stara_y
        elif element["typ"] == "kamien":
            koszt += element["wartosc"]
            powod_dodatkowy = " (jechal przez kamieniste pole -5 energii)"
            element["uzyty"] = True
        elif element["typ"] == "panel":
            lazik.energia += element["wartosc"]
            powod_dodatkowy = f" (+{element['wartosc']} energii z panelu slonecznego)"
            lazik.zaliczone_panele += 1
            element["uzyty"] = True
        elif element["typ"] == "probka":
            lazik.zebrane_probki += 1
            powod_dodatkowy = " (zebrano probke skaly!)"
            element["uzyty"] = True
        elif element["typ"] == "stacja":
            powod_dodatkowy = " (DOTARL DO STACJI METEOROLOGICZNEJ!)"
            element["uzyty"] = True

    lazik.energia -= koszt
    lazik.x = nowa_x
    lazik.y = nowa_y
    lazik.trasa.append((nowa_x, nowa_y))

    opis = (f"  Ruch ({stara_x}, {stara_y}) -> ({nowa_x}, {nowa_y}). "
            f"Energia: {stara_energia} => {lazik.energia} (-{koszt}){powod_dodatkowy}")
    return opis


def skret(lazik, w_lewo):
    stary = lazik.kat
    if w_lewo:
        lazik.kat = (lazik.kat + 30) % 360
        return f"  Skret w lewo: kat {stary} => {lazik.kat} stopni"
    else:
        lazik.kat = (lazik.kat - 30) % 360
        return f"  Skret w prawo: kat {stary} => {lazik.kat} stopni"


def odpoczynek(lazik):
    stara = lazik.energia
    # nie pozwalamy przekroczyc 150% wartosci startowej
    maks = int(lazik.energia_start * 1.5)
    lazik.energia = min(maks, lazik.energia + 8)
    przyrost = lazik.energia - stara
    return (f"  Odpoczynek: panele lazika ladowaly. "
            f"Energia: {stara} => {lazik.energia} (+{przyrost})")


def skanowanie(lazik, swiat):
    lazik.energia -= 1
    # wypisujemy co widac w promieniu 15 jednostek
    znalezione = []
    for e in swiat.elementy:
        if e["uzyty"] and e["typ"] != "krater":
            continue
        d = math.sqrt((e["x"] - lazik.x) ** 2 + (e["y"] - lazik.y) ** 2)
        if d <= 15:
            znalezione.append((d, e))
    znalezione.sort(key=lambda para: para[0])

    linie = [f"  Skan okolic (koszt 1 energii, zostalo: {lazik.energia})"]
    if not znalezione:
        linie.append("    nic ciekawego w poblizu")
    else:
        for d, e in znalezione:
            linie.append(f"    - {e['typ']} na ({e['x']}, {e['y']}), odleglosc {round(d, 1)}")
    return "\n".join(linie)
