# Wypisywanie naglowka wyprawy i raportu koncowego.


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
BLUE = "\033[38;5;75m"
GREEN = "\033[92m"
YELLOW = "\033[38;5;180m"
RED = "\033[91m"
WHITE = "\033[38;5;252m"


def koloruj(tekst, kolor, pogrub=False):
    start = kolor
    if pogrub:
        start += BOLD
    return f"{start}{tekst}{RESET}"


def wypisz_naglowek(lazik, swiat, cel_x, cel_y, limit_krokow):
    print()
    print(koloruj("=" * 60, BLUE, True))
    print(koloruj("   START WYPRAWY", CYAN, True))
    print(koloruj("=" * 60, BLUE, True))
    print(koloruj(f"  Nazwa lazika      : {lazik.nazwa}", WHITE))
    print(koloruj(f"  Pozycja startowa  : ({lazik.x}, {lazik.y})", WHITE))
    print(koloruj(f"  Kat startowy      : {lazik.kat} stopni", WHITE))
    print(koloruj(f"  Energia startowa  : {lazik.energia}", WHITE))
    print(koloruj(f"  Rozmiar swiata    : od -{swiat.rozmiar} do {swiat.rozmiar}", WHITE))
    print(koloruj(f"  Cel (stacja met.) : ({cel_x}, {cel_y})", WHITE))
    print(koloruj(f"  Limit krokow      : {limit_krokow}", WHITE))
    print()
    print(koloruj("  Warunki zakonczenia:", YELLOW, True))
    print(koloruj("   - dotarcie do stacji meteorologicznej (SUKCES)", GREEN))
    print(koloruj("   - calkowite wyczerpanie energii (PORAZKA)", RED))
    print(koloruj("   - przekroczenie limitu krokow (PORAZKA)", RED))
    print(koloruj("   - proba opuszczenia obszaru mapy zostaje zablokowana", WHITE))
    print(koloruj("=" * 60, BLUE, True))
    print()


def wypisz_pomoc_akcji():
    print()
    print(koloruj("Dostepne akcje:", YELLOW, True))
    print(koloruj("  w - jedz do przodu (5 jednostek, koszt 5 energii)", WHITE))
    print(koloruj("  a - skrec w lewo o 30 stopni", WHITE))
    print(koloruj("  d - skrec w prawo o 30 stopni", WHITE))
    print(koloruj("  s - odpocznij (lazik laduje 8 energii)", GREEN))
    print(koloruj("  k - skanuj okolice (pokazuje pobliskie elementy, koszt 1 energii)", WHITE))
    print(koloruj("  q - zakoncz wyprawe wczesniej", RED))
    print()


def policz_wynik(lazik, wynik):

    # probka 10pkt
    # panel 5pkt
    # krater -8pkt


    punkty = 0
    if wynik == "SUKCES":
        punkty += 200
    punkty += lazik.zebrane_probki * 10
    punkty += lazik.zaliczone_panele * 5
    punkty -= lazik.uderzenia_w_krater * 8
    # bonus za pozostala energie
    punkty += max(0, lazik.energia) // 5
    return punkty


def wypisz_raport(lazik, swiat, cel_x, cel_y, limit_krokow, wynik, powod):
    print()
    print(koloruj("=" * 60, BLUE, True))
    print(koloruj("   RAPORT KONCOWY WYPRAWY", CYAN, True))
    print(koloruj("=" * 60, BLUE, True))
    print(koloruj(f"  Nazwa lazika           : {lazik.nazwa}", WHITE))
    print()
    print(koloruj("  Parametry poczatkowe:", YELLOW, True))
    print(koloruj(f"    pozycja startowa     : ({lazik.x_start}, {lazik.y_start})", WHITE))
    print(koloruj(f"    kat startowy         : {lazik.kat_start} stopni", WHITE))
    print(koloruj(f"    energia startowa     : {lazik.energia_start}", WHITE))
    print(koloruj(f"    rozmiar swiata       : {swiat.rozmiar}", WHITE))
    print(koloruj(f"    cel                  : ({cel_x}, {cel_y})", WHITE))
    print(koloruj(f"    limit krokow         : {limit_krokow}", WHITE))
    print()
    print(koloruj("  Wyniki:", YELLOW, True))
    print(koloruj(f"    koncowa pozycja      : ({lazik.x}, {lazik.y})", WHITE))
    print(koloruj(f"    koncowy kat          : {lazik.kat} stopni", WHITE))
    print(koloruj(f"    wykonane kroki       : {lazik.kroki}", WHITE))
    print(koloruj(f"    pozostala energia    : {lazik.energia}", GREEN if lazik.energia > 0 else RED, True))
    print(koloruj(f"    zebrane probki       : {lazik.zebrane_probki}", GREEN if lazik.zebrane_probki > 0 else WHITE))
    print(koloruj(f"    zaladowano z paneli  : {lazik.zaliczone_panele} razy", GREEN if lazik.zaliczone_panele > 0 else WHITE))
    print(koloruj(f"    uderzenia w kratery  : {lazik.uderzenia_w_krater}", RED if lazik.uderzenia_w_krater > 0 else WHITE))
    print()

    print(koloruj("  Najwazniejsze wpisy z dziennika:", YELLOW, True))
    waznosci = [w for w in lazik.dziennik if (">>" in w or "ZDARZENIE" in w
                                              or "DOTARL" in w
                                              or "probke" in w
                                              or "panelu" in w)]
    if not waznosci:
        print(koloruj("    (brak istotnych zdarzen)", WHITE))
    else:
        for w in waznosci[:15]:
            kolor = WHITE
            tekst = w.lower()
            if "dotarl" in tekst or "probke" in tekst or "panelu" in tekst or "energia +" in tekst:
                kolor = GREEN
            elif "zdarzenie" in tekst or "burza" in tekst or "usterka" in tekst or "krater" in tekst:
                kolor = RED
            print(koloruj(f"    - {w}", kolor))
        if len(waznosci) > 15:
            print(koloruj(f"    ... oraz {len(waznosci) - 15} innych wpisow", WHITE))
    print()

    print(koloruj(f"  Przyczyna zakonczenia : {powod}", WHITE))
    punkty = policz_wynik(lazik, wynik)
    kolor_wyniku = WHITE
    if wynik == "SUKCES":
        kolor_wyniku = GREEN
    elif wynik == "PORAZKA":
        kolor_wyniku = RED
    print(koloruj(f"  Wynik wyprawy         : {wynik}", kolor_wyniku, True))
    print(koloruj(f"  Liczba punktow        : {punkty}", CYAN, True))

    # opisowa ocena
    if wynik == "SUKCES":
        if punkty >= 280:
            print(koloruj("  Ocena                 : doskonala wyprawa!", GREEN, True))
        elif punkty >= 220:
            print(koloruj("  Ocena                 : udana misja", GREEN, True))
        else:
            print(koloruj("  Ocena                 : czesciowy sukces, ale do celu dotarl", YELLOW, True))
    elif wynik == "PRZERWANIE":
        print(koloruj("  Ocena                 : misja przerwana przez operatora", YELLOW, True))
    else:
        if lazik.zebrane_probki >= 2:
            print(koloruj("  Ocena                 : porazka, ale udalo sie zebrac probki", YELLOW, True))
        else:
            print(koloruj("  Ocena                 : porazka", RED, True))
    print(koloruj("=" * 60, BLUE, True))
    print()
