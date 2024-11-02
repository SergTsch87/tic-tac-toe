#!usr/bin/env
import pygame, sys

import pygame.draw_py

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

SCREEN_WIDTH, SCREEN_HIGHT = 600, 600
LINE_WIDTH = 15
CELL_SIZE = 200
BOARD_SIZE = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOWER_COLOR = (150, 150, 150)
BASE_COLOR = WHITE

pygame.init()


# представляє ігрове поле
class Board:
    def __init__(self, size = BOARD_SIZE) -> None:
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        # self.winning_line_drawn = False

    def reset(self):
        self.board = [["" for _ in range(self.size)] for _ in range(self.size)]

    def draw_winning_line(self, dict_winning_coords, screen):
        # if self.winning_line_drawn:
        #     return # Якщо лінію вже намальовано, тоді виходимо (щоб не було перемальовок лінії)
        num_col = dict_winning_coords['col']
        num_row = dict_winning_coords['row']
        # print(f'num_col == {num_col}')
        # print(f'num_row == {num_row}')
        
        if num_col >= 0: # vert            
            pygame.draw.line(screen, BLACK, (num_col * CELL_SIZE + 100, 10), 
                                          (num_col * CELL_SIZE + 100, self.size * CELL_SIZE - 10), LINE_WIDTH)
        elif num_row >= 0: # horz
            pygame.draw.line(screen, BLACK, (10, num_row * CELL_SIZE + 100), 
                                          (self.size * CELL_SIZE - 10, num_row * CELL_SIZE + 100), LINE_WIDTH)
            
        # elif num_row == -1 and num_col == 3: # head diag
        elif num_row == -3 and num_col == -3: # head diag
            pygame.draw.line(screen, BLACK, (10, 10), 
                                          (self.size * CELL_SIZE - 10, self.size * CELL_SIZE - 10), LINE_WIDTH)
        
        # elif num_row == 3 and num_col == -1: # scnd diag
        elif num_row == -2 and num_col == -2: # scnd diag
            pygame.draw.line(screen, BLACK, (self.size * CELL_SIZE - 10, 10), 
                                          (10, self.size * CELL_SIZE - 10), LINE_WIDTH)
            
        # self.winning_line_drawn = True # Встановлюємо прапорець, щоб лінію не перемальовувати

    def draw_x(self, screen, col, row):
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 40, row * CELL_SIZE + 20), 
                                      ((col + 1) * CELL_SIZE - 40, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
        
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 40, (row + 1) * CELL_SIZE - 20),
                                      ((col + 1) * CELL_SIZE - 40, row * CELL_SIZE + 20), LINE_WIDTH)

    def draw_0(self, screen, col, row):
        pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), (CELL_SIZE // 2 - 20), LINE_WIDTH)

    def draw_x_or_0(self, screen, row, col):
        if self.board[row][col] == "X":
            self.draw_x(screen, col, row)
        elif self.board[row][col] == "0":
            self.draw_0(screen, col, row)

    def draw_grid(self, screen):
        for row in range(1, self.size):
            pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HIGHT), LINE_WIDTH)

    # Малює сітку та символи на полі
    def draw(self, screen, dict_winning_coords):
        self.draw_grid(screen)

        for row in range(self.size):
            for col in range(self.size):
                self.draw_x_or_0(screen, row, col)

        self.draw_winning_line(dict_winning_coords, screen)

    # Вставити символ у порожню чарунку
    def update(self, row, col, player_symbol):
        if self.board[row][col] == "":
            self.board[row][col] = player_symbol
            return True
        
        return False
    

    def check_win(self, player_symbol, dict_winning_coords):
        # Перевірка по рядках, стовпцях та діагоналях
        for row in range(self.size):
            if all(self.board[row][col] == player_symbol for col in range(self.size)):
                dict_winning_coords["row"] = row
                return True, dict_winning_coords
            
        for col in range(self.size):
            if all(self.board[row][col] == player_symbol for row in range(self.size)):
                dict_winning_coords["col"] = col
                return True, dict_winning_coords

        if all(self.board[i][i] == player_symbol for i in range(self.size)):
            # dict_winning_coords = {'row': -1, 'col': 3}
            dict_winning_coords = {'row': -3, 'col': -3}
            return True, dict_winning_coords
            # return True, {'row': -1, 'col': 3}
        
        elif all(self.board[i][self.size - i - 1] == player_symbol for i in range(self.size)):
            dict_winning_coords = {'row': -2, 'col': -2}
            # dict_winning_coords = {'row': 3, 'col': -1}
            return True, dict_winning_coords
            # return True, {'row': 3, 'col': -1}
        
        return False, dict_winning_coords
    

    # Перевіряє, чи заповнено матрицю (список списків) поля
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


    def process_turn(self, clicked_row, clicked_col, count_step, dict_winning_coords):
        if self.board.update(clicked_row, clicked_col, self.players[self.currrent_player_index].symbol):
            count_step += 1
            # print(f'count_step == {count_step}')

            # Оновлення словника dict_winning_coords
            has_winner, dict_winning_coords = self.board.check_win(self.players[self.currrent_player_index].symbol, dict_winning_coords)
            # print(f'\nIntro process_turn: dict_winning_coords == {dict_winning_coords}\n')

            if count_step > 4 and has_winner:
                self.game_over = True
                self.winner = self.players[self.currrent_player_index].symbol
                print(f'winner == {self.winner}')
            elif count_step == 9 and self.board.is_full():
                self.game_over = True
                self.winner = "Draw"
                print(f'winner == "Draw"')
            else:
                self.switch_player()
                print('else: switch_player()')
        
        return self.game_over, self.winner, count_step, dict_winning_coords

    def change_color(self, rect, mouse_pos):
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOWER_COLOR, rect)
        else:
            pygame.draw.rect(self.screen, BASE_COLOR, rect)

    def change_color_for_rects(self, mouse_pos):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.change_color(rect, mouse_pos)

    def run(self):
        running = True
        count_step = 0
        dict_winning_coords = {'row': -1, 'col': -1}

        while running:
            # self.board.draw(self.screen, dict_winning_coords)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                mouse_pos = pygame.mouse.get_pos()
                # Очищення екрану
                self.screen.fill(WHITE)
                
                self.change_color_for_rects(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouse_x, mouse_y = event.pos
                    clicked_row = mouse_y // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE

                    self.game_over, self.winner, count_step, dict_winning_coords = self.process_turn(clicked_row, clicked_col, count_step, dict_winning_coords)
                    
            # Малювання дошки поверх усього екрану
            self.board.draw(self.screen, dict_winning_coords)
            # Оновлення дисплею
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    # game = Game()
    # game.run()
    
    # # # tmp_list = ['', 0, 1]
    # # # tmp_list = [0, 0, 1]
    # # tmp_list = [1, 0, 1]
    # # print(f'all(tmp_list) == {all(tmp_list)}')

    list_lines = [[0, 1, 0], [1, 0, -1], [1, 1, 0]]
    # list_lines = [[1, 0, 0], [1, 1, 0], [0, 0, 1]]
    flat_list_lines = [elem for sublist in list_lines for elem in sublist] # 511 можливих комбінацій
    
    list_winner_indexes = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
    # Чи мо, краще створити такий список?:
        # list_winner_indexes = ['123', '456', '789', '147', '258', '369', '159', '357']

    len_flat_list_lines = len(flat_list_lines)
    # list_indexes_x = []
    # list_indexes_0 = []
    
    # Оптимізуй це!
    # Збираємо списки індексів іксів та нулів відповідно
    list_indexes_x = [x[0] + 1 for x in enumerate(flat_list_lines) if x[1]]
    print(f'list_indexes_x == {list_indexes_x}') # [1, 4, 5, 9]

    list_indexes_0 = [y[0] + 1 for y in enumerate(flat_list_lines) if y[1] == 0]
    print(f'list_indexes_0 == {list_indexes_0}') # [2, 3, 6, 7, 8]

    set_indexes_x = set(list_indexes_x)
    set_indexes_0 = set(list_indexes_0)

    list_0 = [item for item in list_winner_indexes if set(item).isdisjoint(set_indexes_x)]
    print(f'list_0 == {list_0}') # []

    list_x = [item for item in list_winner_indexes if set(item).isdisjoint(set_indexes_0)]
    print(f'list_x == {list_x}') # []

    if len(list_0) > 0:
        print('Player_0 this is winner!)')
    elif len(list_x) > 0:
        print('Player_x this is winner!)')
    else:
        print('Draw!')

    # list_indexes_0 = [set_indexes_x and set(item) for item in list_winner_indexes]
    # print(f'list_indexes_0 == {list_indexes_0}') # [{1}, {4, 5}, {9}, {1, 4}, {5}, {9}, {1, 5, 9}, {5}]
    
    # list_indexes_0 = [set_indexes_x & set(item) for item in list_winner_indexes]
    # print(f'list_indexes_0 == {list_indexes_0}') # [{1}, {4, 5}, {9}, {1, 4}, {5}, {9}, {1, 5, 9}, {5}]

        # list_indexes_x = [x[0] for x in enumerate(flat_list_lines) if x]
        # print(f'list_indexes_x == {list_indexes_x}') # [0, 1, 2, 3, 4, 5, 6, 7, 8]

        # list_indexes_x = [x for x in flat_list_lines if x]
        # print(f'list_indexes_x == {list_indexes_x}') # [1, 1, 1, 1]

        # list_indexes_x = list(enumerate(flat_list_lines))
        
        # print(f'list_indexes_x == {list_indexes_x}')
        # print(f'list_indexes_x[3][0] == {list_indexes_x[3][0]}')
        # print(f'list_indexes_x[3][1] == {list_indexes_x[3][1]}')
        
    # for item in range(len_flat_list_lines):
    #     if item == '0':
    #         list_indexes_0.append(item + 1)
    #     elif item == 'x':
    #         list_indexes_x.append(item + 1)

    # Задача:
    # Порівняти список довжиною 2..5 ел-тів, зі списком списків list_winner_indexes
    # len_list_winner_indexes = len(list_winner_indexes)
    # len_list_indexes_x = len(list_indexes_x)
    
    # for item in list_indexes_x:
    #     for elem in list_winner_indexes:
    #         if item in elem:
    #             # вилучаємо трійку індексів, які є в elem
    #             pass
    
    # Також, створимо список для "0", в якому залишимо тіко ті ел-ти списку list_winner_indexes, індексів яких немає у списку list_indexes_x.
    # Тобто, наприклад:
    #     list_indexes_x = [2,3,4,5]
    # Тоді для нулів залишається тіко [7,8,9], бо усі інші ел-ти мають у своєму складі хоча б одне з чисел списку list_indexes_x.
    # Такий спосіб повинен зменшити к-сть перевірок для list_indexes_0

# 2-й спосіб:

# # 1-й спосіб:
#     copy_list_winner_indexes = list_winner_indexes
#     for indexes in list_winner_indexes:
#         # print(f'indexes == {indexes}')
#         # print(f'indexes[0] == {indexes[0]}')
        
#         # new_list - це трійка елементів з flat_list_lines,
#         # індекси яких відповідають елементам відповідного списку трійки з list_winner_indexes
#         new_list = [flat_list_lines[i - 1] for i in indexes]
#         print(f'indexes: new_list == {new_list}, {indexes}')
#         print(f'list_winner_indexes == {list_winner_indexes}')
#         if (len(new_list) == 2 or len(new_list) == 3) and all(new_list) == False:
#             copy_list_winner_indexes.remove(indexes)
#         elif all(new_list):
#             print(f'new_list == {new_list}')
#             print(f'We have a winner == {indexes}')
#             break

#     print(f'copy_list_winner_indexes == {copy_list_winner_indexes}')
        

if __name__ == "__main__":
    main()