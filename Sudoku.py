import pygame
import random
import copy 

WIDTH, HEIGHT = 540, 700 
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 1
THICK_LINE_WIDTH = 3
BOARD_OFFSET_Y = 50 

WHITE = (255, 255, 255)
BLACK = (30, 30, 30) 
LIGHT_GRAY = (220, 220, 220) 
DARK_GRAY = (100, 100, 100) 
BOARD_BG = (240, 240, 240) 
SELECTED_CELL_COLOR = (120, 150, 250) 
USER_NUMBER_COLOR = (50, 50, 200) 
HINT_BG = (180, 220, 255) 
HINT_NUMBER_COLOR = (255, 120, 0) 
ERROR_COLOR = (255, 90, 90) 
SUCCESS_COLOR = (50, 180, 50) 
BUTTON_COLOR = (70, 130, 180) 
BUTTON_HOVER_COLOR = (90, 150, 200) 
BUTTON_TEXT_COLOR = (255, 255, 255) 
FIXED_NUMBER_BG = (230, 230, 230)
# --- Sudoku Core Logic ---
def is_valid(board, num, row, col):
    for x in range(GRID_SIZE):
        if board[row][x] == num and col != x:
            return False
    for x in range(GRID_SIZE):
        if board[x][col] == num and row != x:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num and \
               (start_row + i, start_col + j) != (row, col):
                return False
    return True
def find_empty(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return (r, c)  
    return None
def solve_sudoku(board):
    find = find_empty(board)
    if not find:
        return True 
    row, col = find
    for num in range(1, 10): 
        if is_valid(board, num, row, col):
            board[row][col] = num 
            if solve_sudoku(board): 
                return True
            board[row][col] = 0 
    return False 
def generate_sudoku(difficulty="medium"):
    full_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    def fill_box(board, row_start, col_start):
        nums = random.sample(range(1, 10), 9)
        k = 0
        for r in range(3):
            for c in range(3):
                board[row_start + r][col_start + c] = nums[k]
                k += 1
    fill_box(full_board, 0, 0)
    fill_box(full_board, 3, 3)
    fill_box(full_board, 6, 6)
    solve_sudoku(full_board)
    solved_board_copy = copy.deepcopy(full_board)
    puzzle_board = copy.deepcopy(full_board) 
    if difficulty == "easy":
        num_remove = random.randint(35, 45) 
    elif difficulty == "medium":
        num_remove = random.randint(45, 55)
    elif difficulty == "hard":
        num_remove = random.randint(55, 65) 
    else:
        num_remove = 45 
    cells_to_remove = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cells_to_remove.append((r, c))
    random.shuffle(cells_to_remove)
    count_removed = 0
    for r, c in cells_to_remove:
        if count_removed >= num_remove:
            break
        temp_val = puzzle_board[r][c]
        puzzle_board[r][c] = 0
        count_removed += 1
    initial_board_copy = copy.deepcopy(puzzle_board) 
    return puzzle_board, solved_board_copy, initial_board_copy
def get_possible_values(board, row, col):
    if board[row][col] != 0:
        return set() 
    possible = set()
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            possible.add(num)
    return possible
# --- Pygame GUI ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.font_title = pygame.font.SysFont("Inter", 48, bold=True)
        self.font_large = pygame.font.SysFont("Inter", 40)
        self.font_medium = pygame.font.SysFont("Inter", 24)
        self.font_small = pygame.font.SysFont("Inter", 18)
        self.board, self.solved_board, self.initial_board = generate_sudoku("easy")
        self.selected_cell = None 
        self.running = True
        self.message = "" 
        self.message_color = BLACK
        self.hint_cell = None
        self.hint_value = None
        self.HINT_DISPLAY_TIME = 100 
        button_width_hint = 100
        button_width_solve = 100
        button_width_new_game = 150
        button_spacing = 10
        total_buttons_width = button_width_hint + button_spacing + button_width_solve + button_spacing + button_width_new_game
        buttons_start_x = (WIDTH - total_buttons_width) // 2
        self.buttons = {
            "Hint": pygame.Rect(buttons_start_x, HEIGHT - 50, button_width_hint, 40),
            "Solve": pygame.Rect(buttons_start_x + button_width_hint + button_spacing, HEIGHT - 50, button_width_solve, 40),
            "New Game": pygame.Rect(buttons_start_x + button_width_hint + button_spacing + button_width_solve + button_spacing, HEIGHT - 50, button_width_new_game, 40),
        }
        self.button_hover_state = {name: False for name in self.buttons} 
        self.board_display_x_offset = (WIDTH - (GRID_SIZE * CELL_SIZE)) // 2
    def draw_button(self, rect, text, is_hovered):
        shadow_offset = 3
        shadow_color = (50, 50, 50)
        pygame.draw.rect(self.screen, shadow_color, (rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height), 0, border_radius=10)
        btn_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(self.screen, btn_color, rect, 0, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10) 
        text_surface = self.font_medium.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    def draw_grid(self):
        self.screen.fill(WHITE)
        title_surface = self.font_title.render("Sudoku Game", True, BLACK) 
        title_rect = title_surface.get_rect(center=(WIDTH // 2, BOARD_OFFSET_Y // 2))
        self.screen.blit(title_surface, title_rect)
        board_rect_coords = (self.board_display_x_offset, BOARD_OFFSET_Y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        pygame.draw.rect(self.screen, BOARD_BG, board_rect_coords) 
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_x = self.board_display_x_offset + c * CELL_SIZE
                cell_y = BOARD_OFFSET_Y + r * CELL_SIZE
                if self.initial_board[r][c] != 0:
                    pygame.draw.rect(self.screen, FIXED_NUMBER_BG, (cell_x + LINE_WIDTH, cell_y + LINE_WIDTH, CELL_SIZE - 2 * LINE_WIDTH, CELL_SIZE - 2 * LINE_WIDTH))
                current_num = self.board[r][c]
                if current_num != 0:
                    text_color = BLACK 
                    if (r, c) == self.hint_cell and current_num == self.hint_value:
                        text_color = HINT_NUMBER_COLOR
                    elif self.initial_board[r][c] == 0: 
                        text_color = USER_NUMBER_COLOR
                    text_surface = self.font_large.render(str(current_num), True, text_color)
                    text_rect = text_surface.get_rect(center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                    self.screen.blit(text_surface, text_rect)
        for i in range(GRID_SIZE + 1):
            line_color = LIGHT_GRAY
            thickness = LINE_WIDTH
            pygame.draw.line(self.screen, line_color, 
                             (self.board_display_x_offset, BOARD_OFFSET_Y + i * CELL_SIZE), 
                             (self.board_display_x_offset + GRID_SIZE * CELL_SIZE, BOARD_OFFSET_Y + i * CELL_SIZE), thickness)
            pygame.draw.line(self.screen, line_color, 
                             (self.board_display_x_offset + i * CELL_SIZE, BOARD_OFFSET_Y), 
                             (self.board_display_x_offset + i * CELL_SIZE, BOARD_OFFSET_Y + GRID_SIZE * CELL_SIZE), thickness)
        for i in range(0, GRID_SIZE + 1, 3):
            thickness = THICK_LINE_WIDTH
            line_color = DARK_GRAY
            pygame.draw.line(self.screen, line_color, 
                             (self.board_display_x_offset, BOARD_OFFSET_Y + i * CELL_SIZE), 
                             (self.board_display_x_offset + GRID_SIZE * CELL_SIZE, BOARD_OFFSET_Y + i * CELL_SIZE), thickness)
            pygame.draw.line(self.screen, line_color, 
                             (self.board_display_x_offset + i * CELL_SIZE, BOARD_OFFSET_Y), 
                             (self.board_display_x_offset + i * CELL_SIZE, BOARD_OFFSET_Y + GRID_SIZE * CELL_SIZE), thickness)
        if self.selected_cell:
            r, c = self.selected_cell
            highlight_x = self.board_display_x_offset + c * CELL_SIZE + LINE_WIDTH
            highlight_y = BOARD_OFFSET_Y + r * CELL_SIZE + LINE_WIDTH
            highlight_size = CELL_SIZE - 2 * LINE_WIDTH
            pygame.draw.rect(self.screen, SELECTED_CELL_COLOR, 
                             (highlight_x, highlight_y, highlight_size, highlight_size), 
                             3, border_radius=5) 
        if self.hint_cell:
            r, c = self.hint_cell
            cell_x = self.board_display_x_offset + c * CELL_SIZE
            cell_y = BOARD_OFFSET_Y + r * CELL_SIZE
            pygame.draw.rect(self.screen, HINT_BG, (cell_x + LINE_WIDTH, cell_y + LINE_WIDTH, CELL_SIZE - 2 * LINE_WIDTH, CELL_SIZE - 2 * LINE_WIDTH), 0) 

        pygame.draw.rect(self.screen, DARK_GRAY, board_rect_coords, 5, border_radius=10) 
        message_surface = self.font_medium.render(self.message, True, self.message_color)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT - 80)) 
        self.screen.blit(message_surface, message_rect)
        for name, rect in self.buttons.items():
            self.draw_button(rect, name, self.button_hover_state[name])
        pygame.display.flip() 
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEMOTION: 
            for name, rect in self.buttons.items():
                self.button_hover_state[name] = rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for name, rect in self.buttons.items():
                if rect.collidepoint(x, y):
                    if name == "Hint":
                        self.provide_hint()
                    elif name == "Solve":
                        self.solve_game()
                    elif name == "New Game":
                        self.start_new_game()
                    return 
            board_x = x - self.board_display_x_offset
            board_y = y - BOARD_OFFSET_Y 
            col = board_x // CELL_SIZE
            row = board_y // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if self.initial_board[row][col] == 0: 
                    self.selected_cell = (row, col)
                    self.message = "" 
                    self.message_color = BLACK
                    self.hint_cell = None 
                    self.hint_value = None
                else:
                    self.selected_cell = None 
                    self.message = "Cannot change original numbers."
                    self.message_color = ERROR_COLOR 
        if event.type == pygame.KEYDOWN:
            if self.selected_cell:
                r, c = self.selected_cell
                self.hint_cell = None 
                self.hint_value = None
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = int(event.unicode) 
                    self.board[r][c] = num 
                    if not is_valid(self.board, num, r, c):
                        self.message = "Invalid move!"
                        self.message_color = ERROR_COLOR
                    else:
                        self.message = ""
                        self.message_color = BLACK 
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.board[r][c] = 0
                    self.message = ""
                    self.message_color = BLACK
            if event.key == pygame.K_h: 
                self.provide_hint()
            elif event.key == pygame.K_s: 
                self.solve_game()
            elif event.key == pygame.K_n: 
                self.start_new_game()
    def provide_hint(self):
        self.message = ""
        self.message_color = BLACK
        self.hint_cell = None
        self.hint_value = None
        empty_cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))

        if not empty_cells:
            self.message = "Puzzle is already solved!"
            self.message_color = SUCCESS_COLOR
            return
        hint_row, hint_col = random.choice(empty_cells)
        possible_values = get_possible_values(self.board, hint_row, hint_col)
        if len(possible_values) == 1:
            hint_val = list(possible_values)[0]
            self.board[hint_row][hint_col] = hint_val
            self.message = "Hint provided!" 
            self.message_color = SUCCESS_COLOR
            self.hint_cell = (hint_row, hint_col)
            self.hint_value = hint_val
            return
        if self.solved_board[hint_row][hint_col] != 0:
            hint_val = self.solved_board[hint_row][hint_col]
            self.board[hint_row][hint_col] = hint_val
            self.message = "Hint provided!"
            self.message_color = SUCCESS_COLOR
            self.hint_cell = (hint_row, hint_col)
            self.hint_value = hint_val
            return
        self.message = "No hints available (or something went wrong with solution)."
        self.message_color = ERROR_COLOR
    def solve_game(self):
        self.board = copy.deepcopy(self.initial_board) 
        temp_board_for_solving = copy.deepcopy(self.initial_board)
        self.selected_cell = None 
        self.hint_cell = None
        self.hint_value = None
        if solve_sudoku(temp_board_for_solving):
            self.board = temp_board_for_solving 
            self.message = "Puzzle solved!"
            self.message_color = SUCCESS_COLOR
        else:
            self.message = "This puzzle is unsolvable."
            self.message_color = ERROR_COLOR
    def start_new_game(self, difficulty="medium"):
        self.board, self.solved_board, self.initial_board = generate_sudoku(difficulty)
        self.selected_cell = None
        self.message = "New game started!"
        self.message_color = BLACK
        self.hint_cell = None 
        self.hint_value = None
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw_grid()
            clock.tick(60) 
        pygame.quit() 
if __name__ == "__main__":
    game = Game()
    game.run()