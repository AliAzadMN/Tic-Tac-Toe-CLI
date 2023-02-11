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


def run_game(game_mode, board) -> None:
    """ The main function of this code that handle most of the tasks """

    if game_mode == 1:
        user_turn, os_turn = set_turn()
    else:
        user_turn, os_turn = 'X', 'O'

    turn = user_turn
    win_combs = ((1, 2, 3), (1, 4, 7), (1, 5, 9), (2, 5, 8), (3, 6, 9), (3, 5, 7), (4, 5, 6), (7, 8, 9), )
    colors = {'X': 'red', 'O': 'green'}

    for step in range(1, 10):
        show_board(board, colors)

        if game_mode == 1 and turn == os_turn:
            os_number = run_robot(user_turn, os_turn, win_combs, board)
            board[os_number] = turn

        else:
            user_number = get_user_number(turn, colors, board)
            board[user_number] = turn

        if step >= 5:  # the game should have at least 5 movements to recognize end game
            win_comb = find_winning_combination(turn, win_combs, board)

            if win_comb or step == 9:  # check the game has a winner or tie
                show_board(board, colors, win_comb)
                return show_final_result(win_comb, game_mode, turn, os_turn)

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


def show_board(board, colors, win_comb=None) -> None:
    """ Show board of the game with some colors """

    os.system('cls')
    print()

    for number in board:

        # if text_color = None -> it means that cell still is empty
        text_color = colors.get(board[number])  # None | red | green

        if text_color and win_comb and number in win_comb:
            text_color = 'blue'

        space = '    ' if number % 3 == 1 else ''
        character = colored(str(board[number]), text_color, attrs=['bold'])
        seprator = '' if number % 3 == 0 else '|'

        print(space, character, seprator, end='\n' if number % 3 == 0 else '', sep='')


def run_robot(user_turn, os_turn, win_combs, board) -> int:
    """ Find the best location for Robot """

    print('\n    Robot is Thinking ...')
    time.sleep(3)

    for turn in (os_turn, user_turn):
        os_number = check_availabe_condition(turn, win_combs, board)

        if os_number:
            return os_number

    return set_random_number(board)


def get_user_number(turn, colors, board) -> int:
    """ Get the location of the cell from the user """

    while True:

        try:
            print(f"\n    {colored(turn, colors[turn], attrs=['bold'])} Move? ", end='')
            user_number = int(input())

            if type(board[user_number]) == int:
                return user_number
            print(colored('\n    That place is alread filled.', 'red'))

        except (ValueError, KeyError):
            print(colored('\n    Please Enter the Number! (Min=1, Max=9)', 'red'))


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


def find_winning_combination(turn, win_combs, board) -> tuple or None:
    """ Find the winning combination if that existed """

    for comb in win_combs:
        if board[comb[0]] == board[comb[1]] == board[comb[2]] == turn:
            return comb


def show_final_result(has_winner, game_mode, turn, os_turn) -> None:
    """
    Show the final result of the game

    if the game has a winner -> has_winner = tuple
    if the game be tied -> has_winner = None
    """

    if has_winner:

        if game_mode == 1:
            print(
                f"\n    {colored('Robot is won', 'blue', attrs=['bold'])}"
                if turn == os_turn else f"\n    {colored('User is won', 'blue', attrs=['bold'])}"
            )
        else:
            print(f"\n    {colored(f'{turn} is won', 'blue', attrs=['bold'])}")

    else:
        print(f"\n    {colored('Tied', 'magenta', attrs=['bold'])}")


def ask_question() -> None:
    """ Ask questions from user to he/she wants play again or not"""

    while True:
        user_input = input('\n    Play Again? (Yes/No): ').lower()

        if user_input in ['yes', 'no']:
            if user_input == 'yes':
                return start()

            return
        print(colored('\n    Invalid input! Please Try again.', 'red'))


if __name__ == "__main__":
    # This code won't run if this file is imported

    # To make the ANSI colors used in termcolor work with Windows terminal
    init()

    start()
