game_board = [[' ', 1, 2, 3], [1, '-', '-', '-'], [2, '-', '-', '-'], [3, '-', '-', '-']]
player_tracker = 1
draw = True


def print_board():
    print()
    print(f'{game_board[0][0]}     {game_board[0][1]}  {game_board[0][2]}  {game_board[0][3]}')
    print()
    print(f'{game_board[1][0]}     {game_board[1][1]}  {game_board[1][2]}  {game_board[1][3]}')
    print(f'{game_board[2][0]}     {game_board[2][1]}  {game_board[2][2]}  {game_board[2][3]}')
    print(f'{game_board[3][0]}     {game_board[3][1]}  {game_board[3][2]}  {game_board[3][3]}')
    print()


print("Let's play TIC TAC TOE!")
print("Type row and column in XX format")
print_board()

while '-' in list(game_board[1][1:] + game_board[2][1:] + game_board[3][1:]):
    if any([game_board[1][1] == 'X' and game_board[1][2] == 'X' and game_board[1][3] == 'X',
            game_board[2][1] == 'X' and game_board[2][2] == 'X' and game_board[2][3] == 'X',
            game_board[3][1] == 'X' and game_board[3][2] == 'X' and game_board[3][3] == 'X',
            game_board[1][1] == 'X' and game_board[2][1] == 'X' and game_board[3][1] == 'X',
            game_board[1][2] == 'X' and game_board[2][2] == 'X' and game_board[3][2] == 'X',
            game_board[1][3] == 'X' and game_board[2][3] == 'X' and game_board[3][3] == 'X',
            game_board[1][1] == 'X' and game_board[2][2] == 'X' and game_board[3][3] == 'X',
            game_board[1][3] == 'X' and game_board[2][2] == 'X' and game_board[3][1] == 'X']):
        print("Player 1 wins")
        draw = False
        break
    if any([game_board[1][1] == 'O' and game_board[1][2] == 'O' and game_board[1][3] == 'O',
            game_board[2][1] == 'O' and game_board[2][2] == 'O' and game_board[2][3] == 'O',
            game_board[3][1] == 'O' and game_board[3][2] == 'O' and game_board[3][3] == 'O',
            game_board[1][1] == 'O' and game_board[2][1] == 'O' and game_board[3][1] == 'O',
            game_board[1][2] == 'O' and game_board[2][2] == 'O' and game_board[3][2] == 'O',
            game_board[1][3] == 'O' and game_board[2][3] == 'O' and game_board[3][3] == 'O',
            game_board[1][1] == 'O' and game_board[2][2] == 'O' and game_board[3][3] == 'O',
            game_board[1][3] == 'O' and game_board[2][2] == 'O' and game_board[3][1] == 'O']):
        print("Player 2 wins")
        draw = False
        break

    if player_tracker == 1:
        p1_move = input("Player 1: ")
        if any([p1_move == '',
                p1_move.isnumeric() is False]):
            print("Incorrect coordinates. Try again")
            continue
        if int(p1_move) not in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
            print("Incorrect coordinates. Try again")
            continue
        elif game_board[int(p1_move[0])][int(p1_move[1])] != '-':
            print("Spot taken. Choose another one")
            continue
        else:
            game_board[int(p1_move[0])][int(p1_move[1])] = 'X'
        player_tracker += 1
        print_board()
    else:
        p2_move = input("Player 2: ")
        if any([p2_move == '',
                p2_move.isnumeric() is False]):
            print("Incorrect coordinates. Try again")
            continue
        if int(p2_move) not in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
            print("Incorrect coordinates. Try again")
            continue
        elif game_board[int(p2_move[0])][int(p2_move[1])] != '-':
            print("Spot taken. Choose another one")
            continue
        else:
            game_board[int(p2_move[0])][int(p2_move[1])] = 'O'
        player_tracker -= 1
        print_board()

if draw:
    print("Draw")
