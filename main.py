#!usr/bin/env
import pygame


# відповідає за основну логіку гри
class Game:
    def __init__(self, currrent_state, action_gamer, count_steps, game_state) -> None:
        self.currrent_state = currrent_state
        self.action_gamer = action_gamer
        self.count_steps = count_steps
        self.game_state = game_state
                            # : win, steps, draw

    def init_game():
        pass

    def change_move():
        pass

    def check_win():
        pass

    def restart_game():
        pass


    # Чергування за допомогою булевої змінної
    def switch_turn(current_turn):
        return not current_turn


# представляє ігрове поле
class Board:
    def __init__(self, size_board, state_cells) -> None:
        self.size_board = size_board
        self.state_cells = state_cells

    def show_board():
        pass

    def update_state_cells():
        pass

    def check_available_steps():
        pass    


# для гравця (наприклад, людина або комп’ютер)
class Player:
    def __init__(self, symbol_gamer, name_gamer, type_gamer) -> None:
        self.symbol_gamer = symbol_gamer
        self.name_gamer = name_gamer
        self.type_gamer = type_gamer # people or pc

    def detect_to_next_step():
        pass


# для зберігання ходів
class Move:
    def __init__(self, coords_step, symbol_gamer) -> None:
        self.coords_step = coords_step
        self.symbol_gamer = symbol_gamer


# для управління грою, валідації ходів та відстеження статусу гри
class GameController:
    def __init__(self) -> None:
        pass

    def process_input():
        pass
    
    def call_check_game():
        pass
    
    def control_stream_game():
        pass
    


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
        # check win or draw
        # update screen

        # show raiting
        # restart game or game over

        current_turn = True # True - гравець "X",  False - гравець "O"
        current_turn = switch_turn(current_turn)
        if current_turn:
            print("Хід гравця X")
        else:
            print("Хід гравця O")


if __name__ == "__main__":
    main()