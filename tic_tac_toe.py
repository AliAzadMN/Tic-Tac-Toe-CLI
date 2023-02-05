from random import randint
from colorama import init
from termcolor import colored
import os
import time


MODES = (
    (1, 2, 3), (1, 4, 7), (1, 5, 9), (2, 5, 8),
    (3, 6, 9), (3, 5, 7), (4, 5, 6), (7, 8, 9),
)
COLOR = {'X': 'red', 'O': 'green'}
win_mode = list()


def start():
    # TODO 0. Change board type to the list
    board = {
        7: 7, 8: 8, 9: 9,
        4: 4, 5: 5, 6: 6,
        1: 1, 2: 2, 3: 3,
    }
    os.system('cls')
    game_mode = get_game_mode()
    run_game(game_mode, board)
    ask_question()


def get_game_mode() -> int:
    """ Get game mode from user """

    while True:
        print("""
Game modes:

    1. Play with Robot 
    2. Play with Each Other 
        """)

        try:
            game_mode = int(input('    Enter the Number: '))

            if game_mode in [1, 2]:
                return game_mode
            print('Please Enter Number [1,2]')

        except ValueError:
            print('Invalid input! Please Try Again.')

        print()


def run_game(game_mode, board):
    if game_mode == 'single':  # TODO 3. Change single to 1
        user_turn, os_turn = set_turn()
    else:
        user_turn, os_turn = 'X', 'O'
    turn = user_turn

    for step in range(1, 10):
        show_board(board)

        if game_mode == 'single':
            run_robot(turn, user_turn, os_turn, board)

        else:
            user_number = get_user_number(turn, board)
            board[user_number] = turn

        if check_end_game(step, game_mode, turn, os_turn, board):
            break

        turn = os_turn if turn == user_turn else user_turn


def set_turn():
    while True:
        print(
            f"\nStart With {colored('X', 'red', attrs=['bold'])} or {colored('O', 'green', attrs=['bold'])}? ", end=''
        )
        user_turn = input()
        user_turn = user_turn.upper()
        if user_turn in ['X', 'O']:
            os_turn = 'O' if user_turn == 'X' else 'X'
            return user_turn, os_turn
        print('Invalid input! Please Try Again.')


def show_board(board):
    os.system('cls')
    for number in board:
        if number in win_mode:  # TODO 1. Using index of list items
            text_color = 'blue'
        elif board[number] == 'X':
            text_color = 'red'
        elif board[number] == 'O':
            text_color = 'green'
        else:
            text_color = None
        # TODO 2. ِDifferent forms(ways) of use colored in termcolor
        print(colored(str(board[number]), text_color, attrs=['bold']), '' if number % 3 == 0 else '|', end='', sep='')
        if number % 3 == 0:
            print()


def run_robot(turn, user_turn, os_turn, board):
    if turn == user_turn:
        user_number = get_user_number(turn, board)
        board[user_number] = turn
    else:
        print('robot is thinking...')
        time.sleep(3)

        for element in (os_turn, user_turn):
            os_number = try_win_self_or_lose_user(element, board)
            if os_number:
                board[os_number] = turn
                return

        random_number = set_random_number(board)
        board[random_number] = turn


def get_user_number(turn, board):
    while True:
        try:
            print(f"{colored(turn, COLOR[turn], attrs=['bold'])} move? ", end='')
            user_number = int(input())
            if type(board[user_number]) == int:
                return user_number
            print('That place is alread filled.')
        except (ValueError, KeyError):
            print('Please Enter the Number! (Min=1, Max=9)')


def try_win_self_or_lose_user(element, board):
    movements = list(filter(lambda number: board[number] == element, board))

    if len(movements) >= 2:
        for mode in MODES:
            temp_list = list(filter(lambda number: number in mode, movements))

            if len(temp_list) == 2:
                empty_position = list(filter(lambda number: number not in temp_list, mode))
                os_number = empty_position[0]

                if type(board[os_number]) == int:
                    return os_number


def set_random_number(board):
    while True:
        random_number = randint(1, 9)
        if type(board[random_number]) == int:
            return random_number


def check_end_game(step, game_mode, turn, os_turn, board):
    result = end_game(step, board)
    if result in [True, False]:
        win_mode.extend(find_out_win_mode(turn, board))
        show_board(board)
        if result:
            if game_mode == 'single':
                print(
                    f"{colored('robot is won', 'blue', attrs=['bold'])}"
                    if turn == os_turn else f"{colored('user is won', 'blue', attrs=['bold'])}"
                )
            else:
                print(colored(turn, COLOR[turn], attrs=['bold']), colored('is won', 'blue', attrs=['bold']))
        else:
            print(f"{colored('Tie', 'magenta')}")

        return True


def end_game(step, board):
    if step >= 5:
        if board[1] == board[2] == board[3]:
            return True
        elif board[1] == board[4] == board[7]:
            return True
        elif board[1] == board[5] == board[9]:
            return True
        elif board[2] == board[5] == board[8]:
            return True
        elif board[3] == board[6] == board[9]:
            return True
        elif board[3] == board[5] == board[7]:
            return True
        elif board[4] == board[5] == board[6]:
            return True
        elif board[7] == board[8] == board[9]:
            return True
        elif step == 9:
            return False


def find_out_win_mode(turn, board):
    for mode in MODES:
        if len(list(filter(lambda x: board[x] == turn, mode))) == 3:
            return mode
    return []


def ask_question():
    while True:
        user_input = input('Play again? (yes/no): ')
        if user_input in ['yes', 'no']:
            if user_input == 'yes':
                win_mode.clear()
                return start()
            return
        print('Invalid input! Please Try again.')


if __name__ == "__main__":
    # This code won't run if this file is imported

    # To make the ANSI colors used in termcolor work with Windows terminal
    init()

    start()
