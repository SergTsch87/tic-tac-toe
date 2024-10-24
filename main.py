#!usr/bin/env
import pygame


# відповідає за основну логіку гри
class Game():
    pass
    # currrent_state
    # action_gamer
    # count_kroks
    # game_state: виграш, ходи, нічия

    # init_game()
    # change_move()
    # check_win()
    # restart_game()


# представляє ігрове поле
class Board():
    pass
    # size_board
    # state_cells

    # show_board()
    # update_state_cells()
    # check_available_kroks()


# для гравця (наприклад, людина або комп’ютер)
class Player():
    pass
    # symbol_gamer
    # name_gamer
    # type_gamer # people or pc

    # detect_to_next_krok()


# для зберігання ходів
class Move():
    pass
    # coords_krok
    # symbol_gamer


# для управління грою, валідації ходів та відстеження статусу гри
class GameController():
    pass
    # process_input()
    # call_check_game()
    # control_stream_game()


def main():
    player_1 = Player() # symbol == X
    player_2 = Player() # symbol == O
    board = Board()

    running = True
    while running:
        pass
        # check onclick or keydown
        # check available to select cell
        # if available cell:
        #     update_board
        #     change action player
        # check win or нічия
        # update screen

        # show raiting
        # restart game or game over

if __name__ == "__main__":
    main()