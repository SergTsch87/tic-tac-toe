#!usr/bin/env
import pygame, sys

import pygame.draw_py


SCREEN_WIDTH, SCREEN_HIGHT = 600, 600
LINE_WIDTH = 15
CELL_SIZE = 200
BOARD_SIZE = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()


# представляє ігрове поле
class Board:
    def __init__(self, size = BOARD_SIZE) -> None:
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]

    def reset(self):
        self.board = [["" for _ in range(self.size)] for _ in range(self.size)]

    # Малює сітку та символи на полі
    def draw(self, screen):
        for row in range(1, self.size):
            pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HIGHT), LINE_WIDTH)

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == "X":
                    pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), 
                                                  ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
                    
                    pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20),
                                                  ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20), LINE_WIDTH)
                elif self.board[row][col] == "0":
                    pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), (CELL_SIZE // 2 - 20), LINE_WIDTH)
    

    # Вставити символ у порожню чарунку
    def update(self, row, col, player_symbol):
        if self.board[row][col] == "":
            self.board[row][col] = player_symbol
            return True
        
        return False
    

    def check_win(self, player_symbol):
        # Перевірка по стовпцях, рядках та діагоналях
        for row in range(self.size):
            if all(self.board[row][col] == player_symbol for col in range(self.size)):
                return True
            
        for col in range(self.size):
            if all(self.board[row][col] == player_symbol for row in range(self.size)):
                return True

        if all(self.board[i][i] == player_symbol for i in range(self.size)) or all(self.board[i][self.size - i - 1] == player_symbol for i in range(self.size)):
            return True
        
        return False
    

    def is_full(self):
        return all(self.board[row][col] != "" for row in range(self.size) for col in range(self.size))


# для гравця (наприклад, людина або комп’ютер)
class Player:
    def __init__(self, symbol) -> None:
        self.symbol = symbol


# відповідає за основну логіку гри
class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.board = Board()
        self.players = [Player("X"), Player("0")]
        self.currrent_player_index = 0
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board.reset()
        self.currrent_player_index = 0
        self.game_over = False
        self.winner = None

    def switch_player(self): # 0 or 1  >>>  "X" or "0"
        self.currrent_player_index = 1 - self.currrent_player_index

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouse_x, mouse_y = event.pos
                    clicked_row = mouse_y // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE

                    if self.board.update(clicked_row, clicked_col, self.players[self.currrent_player_index].symbol):
                        if self.board.check_win(self.players[self.currrent_player_index].symbol):
                            self.game_over = True
                            self.winner = self.players[self.currrent_player_index].symbol
                            print(f'winner == {self.winner}')
                        elif self.board.is_full():
                            self.game_over = True
                            self.winner = "Draw"
                            print(f'winner == "Draw"')
                        else:
                            self.switch_player()
                            print('else: switch_player()')

            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    # game = Game()
    # game.run()

    # board = Board()
    # print(f'board == {board.board}')
    list_lines = [[1, 0, 1], [1, 0, 0], [1, 0, 1]]
    flat_list_lines = [elem for sublist in list_lines for elem in sublist]
    print(f'flat_list_lines == {flat_list_lines}')
    list_indexes = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
    # len_list_indexes = len(list_indexes)
    new_list = []
    # tmp_list = []
    for indexes in list_indexes:
        # tmp_list.append([flat_list_lines[list_indexes[i][0]], flat_list_lines[list_indexes[i][1]], flat_list_lines[list_indexes[i][2]]])
        print(f'indexes == {indexes}')
        print(f'indexes[0] == {indexes[0]}')
        new_list = [flat_list_lines[indexes[0] - 1], flat_list_lines[indexes[1] - 1], flat_list_lines[indexes[2] - 1]]
        print(f'new_list == {new_list}')
        result_winner = list(map(all, new_list))
        if result_winner:
            print(f'result_winner == {result_winner}')
            print(f'new_list == {new_list}')
            return new_list
        new_list = []
    # result_winner = list(map(all, flat_list_lines))
    # print(f'result_winner == {result_winner}')


if __name__ == "__main__":
    main()