# Wizualizacja trasy lazika w oknie turtle.

import turtle

from swiat import KOLORY_ELEMENTOW


def narysuj_trase(lazik, swiat, cel_x, cel_y, tytul):
    # skala - swiat ma rozmiar 'rozmiar', a okno ma okolo 600 pikseli
    skala = 280 / swiat.rozmiar

    ekran = turtle.Screen()
    ekran.setup(width=700, height=700)
    ekran.title(tytul)
    ekran.bgcolor("black")
    ekran.tracer(0, 0)   # wylaczamy animacje, narysujemy wszystko od razu

    # zolw do rysowania osi i granic
    pomocnik = turtle.Turtle()
    pomocnik.hideturtle()
    pomocnik.speed(0)
    pomocnik.color("dimgray")
    pomocnik.penup()

    _rysuj_ramke_i_osie(pomocnik, swiat, skala, tytul)
    _rysuj_elementy(pomocnik, swiat, skala)

    # punkt startowy
    pomocnik.goto(lazik.x_start * skala, lazik.y_start * skala)
    pomocnik.dot(14, "lime")
    pomocnik.goto(lazik.x_start * skala + 8, lazik.y_start * skala + 4)
    pomocnik.write("START", font=("Arial", 9, "bold"))

    # cel
    pomocnik.goto(cel_x * skala + 8, cel_y * skala + 4)
    pomocnik.write("CEL", font=("Arial", 9, "bold"))

    # sama trasa
    rysownik = turtle.Turtle()
    rysownik.hideturtle()
    rysownik.speed(0)
    rysownik.color("orange")
    rysownik.pensize(2)
    rysownik.penup()
    if lazik.trasa:
        x0, y0 = lazik.trasa[0]
        rysownik.goto(x0 * skala, y0 * skala)
        rysownik.pendown()
        for (x, y) in lazik.trasa[1:]:
            rysownik.goto(x * skala, y * skala)
    rysownik.penup()

    # koncowy punkt
    rysownik.goto(lazik.x * skala, lazik.y * skala)
    rysownik.dot(10, "red")
    rysownik.goto(lazik.x * skala + 8, lazik.y * skala - 12)
    rysownik.color("white")
    rysownik.write("KONIEC", font=("Arial", 9, "bold"))

    ekran.update()
    print()
    print("  (Okno turtle otwarte - kliknij na nim, zeby je zamknac)")
    # exitonclick / mainloop moga rzucic rozne wyjatki gdy uzytkownik zamknie
    try:
        ekran.exitonclick()
    except Exception:
        pass
    print("  (Okno turtle zamkniete)")


def _rysuj_ramke_i_osie(t, swiat, skala, tytul):
    # ramka swiata
    r = swiat.rozmiar * skala
    t.goto(-r, -r)
    t.pendown()
    t.pensize(2)
    for _ in range(4):
        t.forward(2 * r)
        t.left(90)
    t.penup()

    # osie X i Y
    t.color("gray25")
    t.goto(-r, 0)
    t.pendown()
    t.goto(r, 0)
    t.penup()
    t.goto(0, -r)
    t.pendown()
    t.goto(0, r)
    t.penup()

    # podpisy
    t.color("white")
    t.goto(r - 10, 5)
    t.write("X", font=("Arial", 10, "normal"))
    t.goto(5, r - 15)
    t.write("Y", font=("Arial", 10, "normal"))
    t.goto(-r, r + 5)
    t.write(tytul, font=("Arial", 12, "bold"))


def _rysuj_elementy(t, swiat, skala):
    for e in swiat.elementy:
        kolor = KOLORY_ELEMENTOW.get(e["typ"], "white")
        t.goto(e["x"] * skala, e["y"] * skala)
        # uzyte elementy lekko przyciemniamy (oprocz kraterow ktore zostaja)
        if e["uzyty"] and e["typ"] != "krater":
            t.dot(6, "gray40")
        else:
            rozmiar_kropki = 12 if e["typ"] == "stacja" else 8
            t.dot(rozmiar_kropki, kolor)
