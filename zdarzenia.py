# Zdarzenia losowe ktore moga sie zdarzyc lazikowi w trakcie ruchu.

import random


def sprobuj_zdarzenie_losowe(lazik):
    """Z pewnym prawdopodobienstwem wystepuje jedno z 4 zdarzen.
    Funkcja zwraca tekst do wypisania, albo None jak nic sie nie stalo."""
    # ok. 20% szans na zdarzenie w danym kroku
    if random.random() > 0.20:
        return None

    typ = random.choice(["burza", "znalezisko", "usterka", "wiatr"])

    if typ == "burza":
        utrata = random.randint(6, 12)
        lazik.energia -= utrata
        return (f"  >> ZDARZENIE: burza pylowa zakryla panele lazika! "
                f"Stracono {utrata} energii.")

    if typ == "znalezisko":
        zysk = random.randint(8, 15)
        lazik.energia += zysk
        return (f"  >> ZDARZENIE: znaleziono zapasowy ogniwo paliwowe. "
                f"Energia +{zysk}.")

    if typ == "usterka":
        # losowy skret z powodu drobnej usterki
        odchylenie = random.choice([-45, -30, 30, 45])
        stary = lazik.kat
        lazik.kat = (lazik.kat + odchylenie) % 360
        return (f"  >> ZDARZENIE: drobna usterka napedu - lazik samoistnie "
                f"skrecil o {odchylenie} stopni ({stary} => {lazik.kat}).")

    # wiatr
    przesuniecie = random.choice([-2, -1, 1, 2])
    os = random.choice(["x", "y"])
    if os == "x":
        lazik.x = round(lazik.x + przesuniecie, 1)
    else:
        lazik.y = round(lazik.y + przesuniecie, 1)
    lazik.trasa.append((lazik.x, lazik.y))
    return (f"  >> ZDARZENIE: silny wiatr przesunal lazik o {przesuniecie} "
            f"jednostek na osi {os.upper()}. Nowa pozycja: ({lazik.x}, {lazik.y}).")
