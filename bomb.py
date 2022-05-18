import numpy as np
import random
import time
from colorama import *
import os
import threading
import keyboard


class Pole:

    def rysuj(self):
        if type(self) == Pole:
            print(Fore.LIGHTYELLOW_EX, end="")
            print("o", end=" ")
            print(Fore.RESET, end="")
        if type(self) == Sciana:
            print(Fore.GREEN, end="")
            print("#", end=" ")
            print(Fore.RESET, end="")


class Agent(Pole):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Duszek(Agent):
    def __init__(self, x, y, hp: int = 1, sila: int = 1):
        super().__init__(x, y)
        self.sila = sila
        self.hp = hp


class Sciana(Pole):
    pass


class Przeszkoda(Pole):
    def __init__(self, typ: int = 0, wytrzymalosc: int = 1):
        self.wytrzymalosc = wytrzymalosc
        self.typ = typ


class Powerup(Pole):
    def __init__(self, nr=0):
        self.nr = nr


class Bomb:
    def __init__(self, x, y, color: int = 0):
        self.x = x
        self.y = y
        self.color = color


class Board:
    s = []
    x_pos = 0
    y_pos = 0
    hp = 6
    points = 0
    sila = 1
    dlugosc = 2
    bomb_list = []
    
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def create(self):
        for i in range(self.height):

            tab = []
            for j in range(self.width):
                tab.append(Pole())
            self.s.append(tab)

    def stan_gry(self):
        print(f"HP = [{self.hp}]", end=" ")
        print(f"POWER = [{self.sila}]", end=" ")
        print(f"LENGTH = [{self.dlugosc-1}]", end=" ")
        print(f"POINTS = [{self.points}]")

    def add_points(self, typ):
        if typ == 0:
            self.points += 1
        elif typ == 1:
            self.points += 3
        elif typ == 2:
            self.points += 5
        elif typ == 3:
            self.hp += 5


def show_board(board):

    while True:
        if board.hp <= 0:
            break
        board.stan_gry()
        welkosc_wyswietlania = 5
        for i in range(board.y_pos-welkosc_wyswietlania, board.y_pos+welkosc_wyswietlania, 1):
            for j in range(board.x_pos-welkosc_wyswietlania, board.x_pos+welkosc_wyswietlania, 1):
                if (i < 0 or i > board.height-1) or (j < 0 or j > board.width-1):
                    pass
                else:
                    zmienna = True
                    for bomb in board.bomb_list:
                        if type(bomb) == Pole:
                            pass
                        elif bomb.x == i and bomb.y == j:
                            if bomb.color == 0:
                                print(Fore.LIGHTYELLOW_EX, end="")
                                print("B", end=" ")
                                print(Fore.RESET, end="")
                            elif bomb.color == 1:
                                print(Fore.YELLOW, end="")
                                print("B", end=" ")
                                print(Fore.RESET, end="")
                            elif bomb.color == 2:
                                print(Fore.RED, end="")
                                print("B", end=" ")
                                print(Fore.RESET, end="")
                            zmienna = False
                            break
                    if zmienna:
                        if type(board.s[i][j]) == Pole:
                            board.s[i][j].rysuj()
                        elif type(board.s[i][j]) == Sciana:
                            board.s[i][j].rysuj()
                        elif type(board.s[i][j]) == Przeszkoda:
                            typ = board.s[i][j].typ

                            if typ == 0:
                                print(Fore.RED, end="")
                                print("*", end=" ")
                            elif typ == 1:
                                print(Fore.LIGHTRED_EX, end="")
                                print("*", end=" ")
                            elif typ == 2:
                                print(Fore.LIGHTCYAN_EX, end="")
                                print("*", end=" ")
                            elif typ == 3:
                                print(Fore.LIGHTWHITE_EX, end="")
                                print("*", end=" ")
                            print(Fore.RESET, end="")

                        elif type(board.s[i][j]) == Agent:

                            print(Fore.BLUE, end="")
                            print("X", end=" ")
                            print(Fore.RESET, end="")
                        elif type(board.s[i][j]) == Powerup:
                            if board.s[i][j].nr == 0:
                                print(Fore.YELLOW, end="")
                                print("+", end=" ")
                                print(Fore.RESET, end="")
                            elif board.s[i][j].nr == 1:
                                print(Fore.GREEN, end="")
                                print("+", end=" ")
                                print(Fore.RESET, end="")
                            elif board.s[i][j].nr == 2:
                                print(Fore.LIGHTMAGENTA_EX, end="")
                                print("+", end=" ")
                                print(Fore.RESET, end="")
                        elif type(board.s[i][j]) == Duszek:
                            print(Fore.LIGHTWHITE_EX, end="")
                            print("D", end=" ")
                            print(Fore.RESET, end="")

            print("")

        #time.sleep(0.2)
        os.system("cls")
    print("Przegrales")


def test_k(board):
    opoznienie = 0.2
    while True:
        try:  # used try so that if user pressed other than the given key error will not be shown

            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                move(board, "s")
                time.sleep(opoznienie)
            if keyboard.is_pressed('d'):
                move(board, "d")
                time.sleep(opoznienie)
            if keyboard.is_pressed('w'):
                move(board, "w")
                time.sleep(opoznienie)
            if keyboard.is_pressed('a'):
                move(board, "a")
                time.sleep(opoznienie)
            if keyboard.is_pressed('f'):
                move(board, "f")
                time.sleep(opoznienie + 0.5)
        except:
            pass


def move(board, klawisz):

    y = board.x_pos
    x = board.y_pos

    if klawisz == "s":
        if type(board.s[x+1][y]) == Sciana or type(board.s[x+1][y]) == Przeszkoda or type(board.s[x+1][y]) == Duszek:
            pass
        elif type(board.s[x+1][y]) == Powerup:
            if board.s[x+1][y].nr == 0:
                board.sila += 1
            elif board.s[x+1][y].nr == 1:
                board.hp += 1
            elif board.s[x+1][y].nr == 2:
                board.dlugosc += 1
            board.s[x+1][y] = Pole()
            buf = board.s[x+1][y]
            board.s[x+1][y] = board.s[x][y]
            board.s[x][y] = buf
            board.y_pos += 1
        else:
            buf = board.s[x+1][y]
            board.s[x + 1][y] = board.s[x][y]
            board.s[x][y] = buf
            board.y_pos += 1

    if klawisz == "w":
        if type(board.s[x-1][y]) == Sciana or type(board.s[x-1][y]) == Przeszkoda or type(board.s[x-1][y]) == Duszek:
            pass
        elif type(board.s[x-1][y]) == Powerup:
            if board.s[x-1][y].nr == 0:
                board.sila += 1
            elif board.s[x-1][y].nr == 1:
                board.hp += 1
            elif board.s[x-1][y].nr == 2:
                board.dlugosc += 1
            board.s[x-1][y] = Pole()
            buf = board.s[x-1][y]
            board.s[x-1][y] = board.s[x][y]
            board.s[x][y] = buf
            board.y_pos -= 1
        else:
            buf = board.s[x - 1][y]
            board.s[x - 1][y] = board.s[x][y]
            board.s[x][y] = buf
            board.y_pos -= 1
    if klawisz == "a":
        if type(board.s[x][y-1]) == Sciana or type(board.s[x][y-1]) == Przeszkoda or type(board.s[x][y-1]) == Duszek:
            pass
        elif type(board.s[x][y-1]) == Powerup:
            if board.s[x][y-1].nr == 0:
                board.sila += 1
            elif board.s[x][y-1].nr == 1:
                board.hp += 1
            elif board.s[x][y-1].nr == 2:
                board.dlugosc += 1
            board.s[x][y - 1] = Pole()
            buf = board.s[x][y - 1]
            board.s[x][y - 1] = board.s[x][y]
            board.s[x][y] = buf
            board.x_pos -= 1
        else:
            buf = board.s[x][y-1]
            board.s[x][y-1] = board.s[x][y]
            board.s[x][y] = buf
            board.x_pos -= 1
    if klawisz == "d":
        if type(board.s[x][y+1]) == Sciana or type(board.s[x][y+1]) == Przeszkoda or type(board.s[x][y+1]) == Duszek:
            pass
        elif type(board.s[x][y+1]) == Powerup:
            if board.s[x][y+1].nr == 0:
                board.sila += 1
            elif board.s[x][y+1].nr == 1:
                board.hp += 1
            elif board.s[x][y+1].nr == 2:
                board.dlugosc += 1
            board.s[x][y + 1] = Pole()
            buf = board.s[x][y + 1]
            board.s[x][y + 1] = board.s[x][y]
            board.s[x][y] = buf
            board.x_pos += 1
        else:
            buf = board.s[x][y + 1]
            board.s[x][y + 1] = board.s[x][y]
            board.s[x][y] = buf
            board.x_pos += 1

    if klawisz == "f":
        bomb_thread = threading.Thread(target=wyb, args=(plansza, x, y))
        bomb_thread.start()


def wyb(board, x, y):
    tim = 1
    if board.bomb_list:
        index = len(board.bomb_list)
    else:
        index = 0

    board.bomb_list.append(Bomb(x, y))
    time.sleep(tim)
    board.bomb_list[index].color = 1
    time.sleep(tim)
    board.bomb_list[index].color = 2
    time.sleep(tim)

    if type(board.s[x][y]) == Agent:
        board.hp -= board.sila
    for i in range(1, board.dlugosc):
        if x-i < 0 or x+i > board.width-1 or y-i<0 or y+i>board.height-1:
            pass
        else:
            if type(board.s[x + i][y]) == Agent:
                board.hp -= board.sila
            if type(board.s[x - i][y]) == Agent:
                board.hp -= board.sila
            if type(board.s[x + i][y]) == Duszek:
                board.s[x + i][y].hp -= board.sila
            if type(board.s[x - i][y]) == Duszek:
                board.s[x - i][y].hp -= board.sila
        if y - i < 0:
            pass
        else:
            if type(board.s[x][y - i]) == Agent:
                board.hp -= board.sila
            if type(board.s[x][y - i]) == Duszek:
                board.s[x][y - i].hp -= board.sila
        if y + i > board.height-1:
            pass
        else:
            if type(board.s[x][y + i]) == Agent:
                board.hp -= board.sila
            if type(board.s[x][y + i]) == Duszek:
                board.s[x][y + i].hp -= board.sila

    for i in range(1, board.dlugosc):
        if type(board.s[x + i][y]) == Przeszkoda:
            board.s[x + i][y].wytrzymalosc -= board.sila
            if board.s[x + i][y].wytrzymalosc <= 0:
                typ = board.s[x + i][y].typ
                board.add_points(typ)
                board.s[x + i][y] = Pole()
    
        if type(board.s[x - i][y]) == Przeszkoda:
            board.s[x - i][y].wytrzymalosc -= board.sila
            if board.s[x - i][y].wytrzymalosc <= 0:
                typ = board.s[x - i][y].typ
                board.add_points(typ)
                board.s[x - i][y] = Pole()
    
        if type(board.s[x][y + i]) == Przeszkoda:
            board.s[x][y + i].wytrzymalosc -= board.sila
            if board.s[x][y + i].wytrzymalosc <= 0:
                typ = board.s[x][y + i].typ
                board.add_points(typ)
                board.s[x][y + i] = Pole()
    
        if type(board.s[x][y - i]) == Przeszkoda:
            board.s[x][y - i].wytrzymalosc -= board.sila
            if board.s[x][y - i].wytrzymalosc <= 0:
                typ = board.s[x][y - i].typ
                board.add_points(typ)
                board.s[x][y - i] = Pole()

    board.bomb_list[index] = Pole()


def duszek(board):
    duszek1 = Duszek(3, 3)
    board.s[3][3] = duszek1
    last_ruch = 0
    tim = 0.5
    while True:

        if duszek1.hp <= 0:
            board.s[duszek1.x][duszek1.y] = Pole()
            board.points += 10
            break
        time.sleep(tim)
        if last_ruch == 1:
            tim = 0.1
            ruch = 0
        else:
            tim = 0.5
            ruch = random.randint(0, 5)
        last_ruch = ruch
        if ruch == 0 or ruch == 3 or ruch == 4:
            kierunek = random.randint(0, 4)
            if kierunek == 0: # dol

                if type(board.s[duszek1.x + 1][duszek1.y]) == Sciana or type(board.s[duszek1.x + 1][duszek1.y]) == Przeszkoda or type(board.s[duszek1.x + 1][duszek1.y]) == Agent:
                    pass
                else:
                    buf = board.s[duszek1.x + 1][duszek1.y]
                    board.s[duszek1.x + 1][duszek1.y] = board.s[duszek1.x][duszek1.y]
                    board.s[duszek1.x][duszek1.y] = buf
                    duszek1.x += 1
            elif kierunek == 1: # gora
                if type(board.s[duszek1.x - 1][duszek1.y]) == Sciana or type(
                        board.s[duszek1.x - 1][duszek1.y]) == Przeszkoda or type(
                        board.s[duszek1.x - 1][duszek1.y]) == Agent:
                    pass
                else:
                    buf = board.s[duszek1.x - 1][duszek1.y]
                    board.s[duszek1.x - 1][duszek1.y] = board.s[duszek1.x][duszek1.y]
                    board.s[duszek1.x][duszek1.y] = buf
                    duszek1.x -= 1
            elif kierunek == 2: # prawo
                if type(board.s[duszek1.x][duszek1.y+1]) == Sciana or type(
                        board.s[duszek1.x][duszek1.y+1]) == Przeszkoda or type(
                        board.s[duszek1.x][duszek1.y+1]) == Agent:
                    pass
                else:
                    buf = board.s[duszek1.x][duszek1.y + 1]
                    board.s[duszek1.x][duszek1.y + 1] = board.s[duszek1.x][duszek1.y]
                    board.s[duszek1.x][duszek1.y] = buf
                    duszek1.y += 1
            elif kierunek == 3: # lewo
                if type(board.s[duszek1.x][duszek1.y - 1]) == Sciana or type(
                        board.s[duszek1.x][duszek1.y - 1]) == Przeszkoda or type(
                        board.s[duszek1.x][duszek1.y - 1]) == Agent:
                    pass
                else:
                    buf = board.s[duszek1.x][duszek1.y - 1]
                    board.s[duszek1.x][duszek1.y - 1] = board.s[duszek1.x][duszek1.y]
                    board.s[duszek1.x][duszek1.y] = buf
                    duszek1.y -= 1
        elif ruch == 1:

            bomb_thread = threading.Thread(target=wyb, args=(plansza, duszek1.x, duszek1.y))
            bomb_thread.start()
        elif ruch == 2:
            pass
        pass


def rozmiesc(plansza, ilosc, width, height):
    for i in range(ilosc):
        x1 = random.randint(0, height-1)
        y1 = random.randint(0, width-1)
        if type(plansza.s[x1][y1]) == Pole:
            typ = random.randint(0, 1)
            if typ == 1:
                n = random.randint(0, 2)
                if n == 0:
                    plansza.s[x1][y1] = Powerup(0)
                elif n == 1:
                    plansza.s[x1][y1] = Powerup(1)
                elif n == 2:
                    plansza.s[x1][y1] = Powerup(2)
            if typ == 0:
                n = random.randint(0, 2)
                if n == 0:
                    plansza.s[x1][y1] = Przeszkoda(0, 1)
                elif n == 1:
                    plansza.s[x1][y1] = Przeszkoda(1, 3)
                elif n == 2:
                    plansza.s[x1][y1] = Przeszkoda(2, 5)
if __name__ == "__main__":
    width = 120
    height = 120
    plansza = Board(width, height)
    plansza.create()
    plansza.s[3][2] = Agent(3, 2)
    plansza.s[5][8] = Przeszkoda(0)
    plansza.s[5][9] = Przeszkoda(1, 3)
    plansza.s[5][10] = Przeszkoda(2, 5)
    plansza.s[5][5] = Przeszkoda(3, 5)

    rozmiesc(plansza, 150, width, height)

    plansza.s[8][3] = Powerup(0)
    plansza.s[7][5] = Powerup(1)
    plansza.s[3][5] = Powerup(2)
    plansza.s[8][5] = Powerup( 2)

    plansza.y_pos = 3
    plansza.x_pos = 2
    for i in range(plansza.width):
        plansza.s[0][i] = Sciana()
        plansza.s[plansza.height-1][i] = Sciana()

    for i in range(plansza.height):
        plansza.s[i][0] = Sciana()
        plansza.s[i][plansza.width-1] = Sciana()
    os.system("cls")

    show_board_thread = threading.Thread(target=show_board, args=(plansza,))
    show_board_thread.start()

    move_board_thread = threading.Thread(target=test_k, args=(plansza,))
    move_board_thread.start()

    duszek_thread = threading.Thread(target=duszek, args=(plansza,))
    duszek_thread.start()


