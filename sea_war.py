from random import randint
board = []
for x in range(6):
    board.append(["O"] * 6)
def print_board(board):
    for row in board:
        print((" ").join(row))
def random_row(board):
    return randint(0, len(board) - 1)
def random_col(board):
    return randint(0, len(board[0]) - 1)
print("Начнем игру в Морской бой!")
print_board(board)
ship_row = random_row(board)
ship_col = random_col(board)
while True:
    for turn in range(10):
        print ("Ход: ", turn)
        guess_row = int(input("Строка 0-5:"))
        guess_col = int(input("Столбец 0-5:"))
        if guess_row == ship_row and guess_col == ship_col:
            print("Поздравляю, ты потопил мой корабль!")
            break
        else:
            if (guess_row < 0 or guess_row > 5) or (guess_col < 0 or guess_col > 5):
                print("Oops, эти координаты не в нашем океане.")
            elif(board[guess_row][guess_col] == "X"):
                print("Эти координаты вы уже называли.")
            else:
                print("Мимо!")
                board[guess_row][guess_col] = "X"
        print_board(board)
        if turn == 9:
            print("Игра окончена! Я уплываю!")
    ga = input('Вы хотите сыграть ещё раз? Если да - нажмите "Enter", если нет - введите "нет" ')
    if ga == 'нет':
        break