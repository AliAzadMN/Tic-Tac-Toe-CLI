from random import randint
from colorama import init
from termcolor import colored
import os
import time


def start():
    # TODO 0. Update

    board = {
        7: 7, 8: 8, 9: 9,
        4: 4, 5: 5, 6: 6,
        1: 1, 2: 2, 3: 3,
    }

    game_mode = get_game_mode()
    run_game(game_mode, board)
    ask_question()


def get_game_mode() -> int:
    """ Get game mode from user """

    while True:
        os.system('cls')

        print("""
    Game modes:

    1. Play with Robot 
    2. Play with Each Other 
        """)

        try:
            game_mode = int(input('    Enter the Number: '))

            if game_mode in [1, 2]:
                return game_mode
            print(colored('\n    Please Enter Number [1,2]', 'red'))

        except ValueError:
            print(colored('\n    Invalid input! Please Try Again.', 'red'))
        time.sleep(2)


def run_game(game_mode, board):
    if game_mode == 1:
        user_turn, os_turn = set_turn()
    else:
        user_turn, os_turn = 'X', 'O'

    turn = user_turn
    win_comb = []
    win_combs = (
        (1, 2, 3), (1, 4, 7), (1, 5, 9), (2, 5, 8), (3, 6, 9), (3, 5, 7), (4, 5, 6), (7, 8, 9),
    )
    colors = {'X': 'red', 'O': 'green'}

    for step in range(1, 10):
        show_board(win_comb, board)

        if game_mode == 1 and turn == os_turn:
            os_number = run_robot(user_turn, os_turn, win_combs, board)
            board[os_number] = turn

        else:
            user_number = get_user_number(turn, colors, board)
            board[user_number] = turn

        if step >= 5:
            has_winner = check_end_game(turn, win_combs, board)

            if has_winner or step == 9:
                win_comb.extend(find_out_win_comb(turn, win_combs, board))
                show_board(win_comb, board)
                show_final_result(has_winner, game_mode, turn, os_turn, colors)
                return

        turn = os_turn if turn == user_turn else user_turn


def set_turn() -> tuple:
    """ Determine turn by user """

    while True:
        time.sleep(2)
        os.system('cls')

        print(
            f"\n    Start with {colored('X', 'red', attrs=['bold'])} or {colored('O', 'green', attrs=['bold'])}? ",
            end=''
        )

        user_turn = input().upper()

        if user_turn in ['X', 'O']:
            os_turn = 'O' if user_turn == 'X' else 'X'
            return user_turn, os_turn

        print(colored('\n    Invalid input! Please Try Again.', 'red'))


def show_board(win_comb, board):
    os.system('cls')
    for number in board:
        if number in win_comb:
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


def run_robot(user_turn, os_turn, win_combs, board) -> int:
    """ Find the best location for Robot """

    print('\n    Robot is Thinking...')
    time.sleep(3)

    for turn in (os_turn, user_turn):
        os_number = check_availabe_condition(turn, win_combs, board)

        if os_number:
            return os_number

    return set_random_number(board)


def get_user_number(turn, colors, board):
    while True:
        try:
            print(f"{colored(turn, colors[turn], attrs=['bold'])} move? ", end='')
            user_number = int(input())
            if type(board[user_number]) == int:
                return user_number
            print('That place is alread filled.')
        except (ValueError, KeyError):
            print('Please Enter the Number! (Min=1, Max=9)')


def check_availabe_condition(turn, win_combs, board) -> int or None:
    """
    Try to win or don't allow to user that win

    1. obtain location of all cells that belong to Robot or User
    2. if location of two cells (belong to Robot or User) was in any of winning combination
    3. if the third cell is empty, return the location of it
    """

    # Location of any cells belong to Robot or User
    locations = list(filter(lambda number: board[number] == turn, board))

    if len(locations) >= 2:

        for comb in win_combs:  # comb -> A winning combination
            location_of_two_cells = list(filter(lambda number: number in comb, locations))

            if len(location_of_two_cells) == 2:

                # Find the location of third cell
                os_number = list(filter(lambda number: number not in location_of_two_cells, comb))[0]

                if type(board[os_number]) == int:
                    return os_number


def set_random_number(board) -> int:
    """ In conditions the cell is empty, return the location of it """

    while True:
        random_number = randint(1, 9)

        if type(board[random_number]) == int:
            return random_number


def check_end_game(turn, win_combs, board) -> bool or None:
    """ Check the game has a winner or not """

    for comb in win_combs:
        if board[comb[0]] == board[comb[1]] == board[comb[2]] == turn:
            return True


def show_final_result(has_winner, game_mode, turn, os_turn, colors) -> None:
    """ Show the final result of the game """

    if has_winner:

        if game_mode == 1:
            print(
                f"{colored('robot is won', 'blue', attrs=['bold'])}"
                if turn == os_turn else f"{colored('user is won', 'blue', attrs=['bold'])}"
            )
        else:
            print(colored(turn, colors[turn], attrs=['bold']), colored('is won', 'blue', attrs=['bold']))

    else:
        print(f"{colored('Tie', 'magenta')}")


def find_out_win_comb(turn, win_combs, board):
    for comb in win_combs:
        if len(list(filter(lambda x: board[x] == turn, comb))) == 3:
            return comb
    return []


def ask_question():
    while True:
        user_input = input('Play again? (yes/no): ')
        if user_input in ['yes', 'no']:
            if user_input == 'yes':
                return start()
            return
        print('Invalid input! Please Try again.')


if __name__ == "__main__":
    # This code won't run if this file is imported

    # To make the ANSI colors used in termcolor work with Windows terminal
    init()

    start()
