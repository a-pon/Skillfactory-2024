from random import randint
import time


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Out of board"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Choose another target"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.health = length

    # orientation: 0 - horizontal, 1 - vertical
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            ship_x = self.bow.x
            ship_y = self.bow.y
            if self.orientation == 0:
                ship_x += i
            elif self.orientation == 1:
                ship_y += i
            ship_dots.append(Dot(ship_x, ship_y))
        return ship_dots


class Board:
    def __init__(self, size, hidden=False):
        self.size = size
        self.hidden = hidden
        self.field = [['\u2b58'] * size for _ in range(size)]
        self.used_dots = []
        self.ships = []
        self.remains = 0

    def __str__(self):
        board_field = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            board_field += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hidden:
            board_field = board_field.replace('\u25a0', '\u2b58')
        return board_field

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_dots:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.y][dot.x] = '\u25a0'
            self.used_dots.append(dot)
        self.ships.append(ship)
        self.remains += 1
        self.contour(ship)

    def contour(self, ship, visible=False):
        c_dots = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        for dot in ship.dots:
            for cx, cy in c_dots:
                d = Dot(dot.x + cx, dot.y + cy)
                if not (self.out(d) or d in self.used_dots):
                    if visible:
                        self.field[d.y][d.x] = ' '
                    self.used_dots.append(d)

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.used_dots:
            raise BoardUsedException()
        self.used_dots.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                self.field[dot.y][dot.x] = 'X'
                ship.health -= 1
                if ship.health > 0:
                    print("Hit")
                else:
                    self.remains -= 1
                    self.contour(ship, True)
                    print("Sunk")
                return True
        self.field[dot.y][dot.x] = 'T'
        print("Miss")
        return False

    def begin(self):
        self.used_dots = []


class Player:
    def __init__(self, board, opponent_board):
        self.board = board
        self.opponent_board = opponent_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.opponent_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        ai_dot = Dot(randint(0, 5), randint(0, 5))
        print(f"Opponent`s move: {ai_dot.x + 1}{ai_dot.y + 1}")
        return ai_dot


class User(Player):
    def ask(self):
        while True:
            user_dot = input("Your move: ")
            if not user_dot.isdecimal() or len(user_dot) != 2:
                print("Incorrect input")
                continue
            return Dot(int(user_dot[0]) - 1, int(user_dot[1]) - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        self.ships = [3, 2, 2, 1, 1, 1, 1]
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hidden = True
        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)

    def try_board(self):
        board = Board(size=self.size)
        attempt = 0
        for length in self.ships:
            while True:
                attempt += 1
                if attempt > 2024:
                    return None
                ship = Ship(length, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    @staticmethod
    def greet():
        print("BATTLESHIP")
        print()
        print("Each player has:")
        print("1x Cruiser (\u25a0 \u25a0 \u25a0)")
        print("2x Destroyer (\u25a0 \u25a0)")
        print("4x Submarine (\u25a0)")
        print()
        print("Input format: XY")
        print("X - column, Y - row")

    def loop(self):
        turn = 0
        while True:
            print()
            if turn % 2 == 0:
                print(self.ai.board)
                repeat = self.user.move()
            else:
                repeat = self.ai.move()
                print(self.user.board)
            if repeat:
                turn -= 1
            if self.user.board.remains == 0:
                print()
                print("You lost")
                break
            if self.ai.board.remains == 0:
                print()
                print(self.ai.board)
                print()
                print("You won")
                break
            turn += 1
            time.sleep(2)

    def start(self):
        self.greet()
        self.loop()


battleship = Game()
battleship.start()
