import random


class Dot:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def input_cell(self):
        while True:
            try:
                self.x = int(input('Введите координату x\t'))
                self.y = int(input('Введите координату y\t'))
                if (0 >= self.x or self.x >= 7) or (0 >= self.y or self.y >= 7):
                    print('Вы ввели некороктные координаты')
                    continue
                else:
                    break
            except ValueError:
                print('Необходимо вводить число')
                continue
        return [self.x, self.y]

    def input_pos(self):
        while True:
            try:
                position = str(input('Введите положение коробля вертикальное (V), горизонтальное (H):\t'))

                if position.upper() != 'H' and position.upper() != 'V':
                    print('Вы ввели некоротные данные позиции, попробуйте еще раз!')
                    continue
                else:
                    break
            except ValueError:
                print('Необходимо вводить букву')
                continue
        return position

    @property
    def get_dot(self):
        return [self.x, self.y]

    def set_dot(self, x, y):
        if (0 >= x or x >= 7) or (0 >= y or y >= 7):
            return 'Введены некороктные координаты'
        else:
            self.x = x
            self.y = y
            return [self.x, self.y]


class Ship:
    def __init__(self, long=0, coord=(), position="", hp=0):
        self.long = long
        self.coord = list(coord)
        self.position = position
        self.hp = hp

    @property
    def dots(self):
        long = self.long
        list_dots = []
        shipparam = []
        for i in range(self.long):
            long = long - 1
            if self.position == 'V':
                list_dots.append([self.coord[0], self.coord[1] + long])
            else:
                list_dots.append([self.coord[0] - long, self.coord[1]])

        shipparam.append(self.long), shipparam.append(list_dots), shipparam.append(self.position), shipparam.append(
            self.hp)
        return shipparam


class ErrorSetupShip(Exception):
    pass


class MissShot(ErrorSetupShip):
    pass


class Board(Dot):
    def __init__(self):
        self.list_board = [['O'] * 6 for i in range(6)]
        self.list_ship = []
        self.list_shots = []

    def setupcheck(self, dots):
        for d in dots:
            y = d[1] - 1
            x = d[0] - 1
            if self.list_board[y][x] == 'O':
                return True
            else:
                return False

    def ship_add(self, ship):
        p = ship[2]
        cell = ship[1]
        long = ship[0]
        try:
            if self.out(cell) == False or self.setupcheck(cell) == False or \
                    self.checkcont(self.contour(long, cell[-1], p)) == False:
                raise ErrorSetupShip

        except ErrorSetupShip:
            return False

        else:
            return True

    def contour(self, long, coord, position):
        x = coord[0]
        y = coord[1]
        combinations = [[x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x - 1, y + 1], [x - 1, y],
                        [x - 1, y - 1], [x, y + 1]]

        for i in range(1):
            if position == 'V':

                for j in range(2, long + 1):
                    combinations.append([x - 1, y + j])
                    combinations.append([x + 1, y + j])

                combinations.remove([x, y + 1])
                combinations.append([x, y + long])
                return combinations
            elif position == 'H':
                for j in range(2, long + 1):
                    combinations.append([x - j, y - 1])
                    combinations.append([x - j, y + 1])

                combinations.remove([x - 1, y])
                combinations.append([x - long, y])
                return combinations

            else:
                return combinations

    def checkcont(self, combinations):
        try:
            for combo in combinations:  # Проверка координат после вычислений на то, чтобы они входили в нужный диапозон
                if (0 >= combo[0] or combo[0] >= 7) or (0 >= combo[1] or combo[1] >= 7):
                    continue
                else:
                    if self.list_board[combo[1] - 1][combo[0] - 1] == '■':
                        raise IndexError

        except IndexError:
            return False

    def draw_board(self):
        _str = '  1|2|3|4|5|6|'
        for draw, num in zip(self.list_board, range(1, 7)):
            _str += '\n' + str(num) + '|'
            for _draw in draw:
                _str += _draw + '|'
        return _str

    def out(self, dot):
        try:
            for c in dot:
                if (0 >= c[0] or c[0] >= 7) or (0 >= c[1] or c[1] >= 7):
                    raise IndexError
                else:
                    return True

        except IndexError:
            return False

    def shot(self, dots, check):
        try:
            y = dots[1] - 1
            x = dots[0] - 1
            if check.list_board[y][x] == 'O':
                raise MissShot
        except MissShot:
            return False

        else:
            return True


class Player:
    def __init__(self):
        self.board = Board()

    def ask_ship(self):
        raise NotImplementedError


class AI(Player):
    def ask_ship(self, long):
        count = 0

        while True:
            if count == 100:
                return False
            else:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                cell = [x, y]
                position = random.choice(['V', 'H'])
                long = long
                ship = Ship(long, cell, position, long)
                try:
                    if self.board.ship_add(ship.dots) == False:
                        raise ErrorSetupShip

                except ErrorSetupShip:
                    count += 1
                    continue
                else:
                    self.board.list_ship.append(ship.dots)
                    for add in ship.dots[1]:
                        self.board.list_board[add[1] - 1][add[0] - 1] = '■'
                    return True

    def ask_shot(self, checklist, drawlist):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        cell = [x, y]
        if cell in self.board.list_shots:
            return self.ask_shot(checklist, drawlist)
        else:
            if self.board.shot(cell, checklist) == True:
                self.board.list_shots.append(cell)
                drawlist.list_board[cell[1] - 1][cell[0] - 1] = 'X'
                for ch in checklist.list_ship:
                    if cell in ch[1]:
                        ch[3] -= 1
                        if ch[3] == 0:
                            print('Ваш корабль потоплен!')
                            print(drawlist.draw_board())
                            print('Противник делает еще один выстрел!')
                            for drawcont in self.board.contour(ch[0], ch[1][-1], ch[2]):
                                if (0 >= drawcont[0] or drawcont[0] >= 7) or (0 >= drawcont[1] or drawcont[1] >= 7):
                                    continue
                                else:
                                    drawlist.list_board[drawcont[1] - 1][drawcont[0] - 1] = 'T'
                            return self.ask_shot(checklist, drawlist)
                        else:
                            print('Ваш корабль подбит!')
                            print(drawlist.draw_board())
                            print('Противник делает еще один выстрел!')
                            return self.ask_shot(checklist, drawlist)

            else:
                drawlist.list_board[cell[1] - 1][cell[0] - 1] = 'T'
                print(drawlist.draw_board())
                print('Ваш противник промахнулся!')


class Human(Player):
    def ask_ship(self, long):
        cell = self.board.input_cell()
        position = 'one' if long == 1 else self.board.input_pos()
        long = long
        ship = Ship(long, cell, position, long)
        try:
            if self.board.ship_add(ship.dots) == False:
                print('Установить корабль нельзя')
                print(self.board.draw_board())
                raise ErrorSetupShip

        except ErrorSetupShip:
            self.ask_ship(long)

        else:
            self.board.list_ship.append(ship.dots)
            for add in ship.dots[1]:
                self.board.list_board[add[1] - 1][add[0] - 1] = '■'
            print(self.board.draw_board())
            return True

    def ask_shot(self, checklist, drawlist):
        cell = self.board.input_cell()
        if cell in self.board.list_shots:
            print('По данным координатам уже был произведен выстрел, введите другие')
            return self.ask_shot(checklist, drawlist)
        else:
            if self.board.shot(cell, checklist) == True:
                self.board.list_shots.append(cell)
                drawlist.list_board[cell[1] - 1][cell[0] - 1] = 'X'
                print(drawlist.draw_board())
                for ch in checklist.list_ship:
                    if cell in ch[1]:
                        ch[3] -= 1
                        if ch[3] == 0:
                            print('Корабль потоплен!')
                            print(drawlist.draw_board())
                            print('Стреляйте еще!')

                            for drawcont in self.board.contour(ch[0], ch[1][-1], ch[2]):
                                if (0 >= drawcont[0] or drawcont[0] >= 7) or (0 >= drawcont[1] or drawcont[1] >= 7):
                                    continue
                                else:
                                    drawlist.list_board[drawcont[1] - 1][drawcont[0] - 1] = 'T'
                            return self.ask_shot(checklist, drawlist)
                        else:
                            print('Корабль подбит!')
                            print('Стреляйте еще!')
                            print(drawlist.draw_board())
                            return self.ask_shot(checklist, drawlist)

            else:
                drawlist.list_board[cell[1] - 1][cell[0] - 1] = 'T'
                print(drawlist.draw_board())
                print('Промах, повезет в следущий раз!')


class Game(Board):
    def __init__(self):
        self.human = Human()
        self.ai = AI()
        self.humanmarks = Human()
        self.aimarks = AI()

    def rules(self):
        print('''Рады приветствовать Вас в игре морской бой!!!
                 ---------------------------------------------
                           П Р А В И Л А   И Г Р Ы
                 ---------------------------------------------

        ''')

    def fill_board(self, player, l):

        if player.ask_ship(l) == False:
            player.board.list_board = [['O'] * 6 for i in range(6)]
            player.board.list_ship = []
            self.setupship()

    def check_win(self):
        checklistai = self.ai.board.list_ship
        checklisthuman = self.human.board.list_ship
        countai = 0
        counthuman = 0

        for scoreai in checklistai:
            if scoreai[3] == 0:
                countai += 1
            else:
                continue

        for scorehuman in checklisthuman:
            if scorehuman[3] == 0:
                counthuman += 1
            else:
                continue

        if counthuman == 7:
            print('Противник одержал победу!')
            return True
        elif countai == 7:
            print('Вы одержали победу')
            return True
        else:
            return False

    def setupship(self):

        self.fill_board(self.ai, 3)

        for i in range(2):
            self.fill_board(self.ai, 2)

        for i in range(4):
            self.fill_board(self.ai, 1)

        print('Введите координаты 3-х палубного коробля')
        self.fill_board(self.human, 3)

        for i in range(2):
            print('Введите координаты 2-х палубного коробля')
            self.fill_board(self.human, 2)

        for i in range(4):
            print('Введите координаты 1 палубного коробля')
            self.fill_board(self.human, 1)
        print('\nПоле противника')
        print(self.humanmarks.board.draw_board())

    def start_shot(self):
        while True:

            if self.check_win() == True:
                print('Игра окончена')
                return True
            else:
                print('Сделайте выстрел!')
                self.human.ask_shot(self.ai.board, self.humanmarks.board)
                print('Противник сделал выстрел!')
                self.ai.ask_shot(self.human.board, self.human.board)

    def gameplay(self):

        self.rules()
        # if self.ask() == True:
        print('Давайте расставим корабли')
        print('Поле ваших кораблей')
        print(self.human.board.draw_board())
        print('Поле противника')
        print(self.humanmarks.board.draw_board())
        self.setupship()
        while True:

            if self.check_win() == True:
                break
            else:
                self.start_shot()
                print('Поле ваших кораблей')
                print(self.human.board.draw_board())
                print('Поле противника')
                print(self.humanmarks.board.draw_board())


games = Game()

games.gameplay()
