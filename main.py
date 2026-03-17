import asyncio
import pygame
import random
import copy
import platform

WIN_W, WIN_H = 540, 660
GRID_PX      = 486
CELL         = GRID_PX // 9
BOARD_X      = (WIN_W - GRID_PX) // 2
BOARD_Y      = 118
BOARD_BOTTOM = BOARD_Y + GRID_PX

BG       = (245, 245, 242)
WHITE    = (255, 255, 255)
BLACK    = (15,  15,  15)
BORDER   = (40,  40,  40)
GRAY_LINE= (195, 195, 190)
GRAY_MID = (140, 140, 136)
GRAY_DARK= (70,  70,  68)

C_FIXED  = (15,  15,  15)
C_USER   = (30,  90, 220)
C_ERROR  = (205, 35,  35)
C_HINT   = (185, 100,  0)
C_SEL    = (208, 226, 255)
C_HL     = (232, 234, 238)
C_SAME   = (190, 212, 255)

BN = (255, 255, 255)
BH = (230, 232, 238)
BA = (20,  20,  20)
BB = (195, 195, 190)

C_OK   = (18, 150, 65)
C_ERR  = (205, 35,  35)
C_WARN = (185, 100,  0)


def is_valid(board, num, row, col):
    for x in range(9):
        if board[row][x] == num and x != col: return False
        if board[x][col] == num and x != row: return False
    sr, sc = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[sr+i][sc+j] == num and (sr+i, sc+j) != (row, col):
                return False
    return True

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0: return (r, c)
    return None

def solve(board):
    e = find_empty(board)
    if not e: return True
    r, c = e
    for n in range(1, 10):
        if is_valid(board, n, r, c):
            board[r][c] = n
            if solve(board): return True
            board[r][c] = 0
    return False

def generate(difficulty):
    full = [[0]*9 for _ in range(9)]
    def fill_box(rs, cs):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                full[rs+i][cs+j] = nums[i*3+j]
    fill_box(0,0); fill_box(3,3); fill_box(6,6)
    solve(full)
    sol    = copy.deepcopy(full)
    puzzle = copy.deepcopy(full)
    cells  = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:{"easy":36,"medium":46,"hard":56}[difficulty]]:
        puzzle[r][c] = 0
    return puzzle, sol, copy.deepcopy(puzzle)


def make_font(size, bold=False):
    for name in ("Segoe UI", "Arial", "Helvetica", "DejaVu Sans", "FreeSans"):
        f = pygame.font.SysFont(name, size, bold=bold)
        if f: return f
    return pygame.font.Font(None, size)


class Button:
    def __init__(self, rect, label, toggle=False):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.toggle  = toggle
        self.active  = False
        self.hovered = False
    def draw(self, surf, font):
        if self.active and self.toggle:
            bg, fg, border = BA, WHITE, BA
        elif self.hovered:
            bg, fg, border = BH, BLACK, GRAY_DARK
        else:
            bg, fg, border = BN, GRAY_DARK, BB
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, border, self.rect, 1, border_radius=8)
        s = font.render(self.label, True, fg)
        surf.blit(s, s.get_rect(center=self.rect.center))
    def hit(self, pos): return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.f_title = make_font(34, bold=True)
        self.f_cell  = make_font(30, bold=True)
        self.f_btn   = make_font(15, bold=False)
        self.f_msg   = make_font(14, bold=False)
        self.board = self.solution = self.initial = None
        self.selected = self.hint_cell = None
        self.difficulty = "easy"
        self.hints_used = 0
        self.done = False
        self.msg, self.msg_col = "", GRAY_MID
        self._build_ui()

    def _build_ui(self):
        bw, bh, gap = 96, 34, 8
        tx = (WIN_W - (3*bw + 2*gap)) // 2
        self.btn_easy   = Button((tx,            62, bw, bh), "Easy",   toggle=True)
        self.btn_medium = Button((tx+bw+gap,     62, bw, bh), "Medium", toggle=True)
        self.btn_hard   = Button((tx+2*(bw+gap), 62, bw, bh), "Hard",   toggle=True)
        self.btn_easy.active = True
        self.diff_btns = [self.btn_easy, self.btn_medium, self.btn_hard]
        self.diff_map  = {self.btn_easy:"easy", self.btn_medium:"medium", self.btn_hard:"hard"}
        abw, abh, agap = 108, 36, 8
        ax = (WIN_W - (4*abw + 3*agap)) // 2
        ay = BOARD_BOTTOM + 16
        self.btn_erase = Button((ax,              ay, abw, abh), "Erase")
        self.btn_hint  = Button((ax+abw+agap,     ay, abw, abh), "Hint")
        self.btn_solve = Button((ax+2*(abw+agap), ay, abw, abh), "Solve")
        self.btn_new   = Button((ax+3*(abw+agap), ay, abw, abh), "New Game")
        self.act_btns = [self.btn_erase, self.btn_hint, self.btn_solve, self.btn_new]
        self.all_btns = self.diff_btns + self.act_btns

    def new_game(self):
        self.board, self.solution, self.initial = generate(self.difficulty)
        self.selected = self.hint_cell = None
        self.hints_used = 0
        self.done = False
        self._msg("")

    def _msg(self, text, color=None):
        self.msg     = text
        self.msg_col = color or GRAY_MID

    def _set_diff(self, btn):
        for b in self.diff_btns: b.active = False
        btn.active = True
        self.difficulty = self.diff_map[btn]

    def enter_num(self, n):
        if not self.selected or self.done or self.board is None: return
        r, c = self.selected
        if self.initial[r][c]: return
        self.board[r][c] = n
        self.hint_cell = None
        if not is_valid(self.board, n, r, c):
            self._msg("Invalid move", C_ERR)
        else:
            self._msg("")
            if self._complete(): self._finish()

    def erase(self):
        if not self.selected or self.done or self.board is None: return
        r, c = self.selected
        if self.initial[r][c]:
            self._msg("Fixed cell", C_ERR); return
        self.board[r][c] = 0
        self.hint_cell = None
        self._msg("")

    def hint(self):
        if self.done or self.board is None: return
        empty = [(r,c) for r in range(9) for c in range(9) if self.board[r][c]==0]
        if not empty: self._msg("Already complete!", C_OK); return
        r, c = random.choice(empty)
        self.board[r][c] = self.solution[r][c]
        self.hint_cell = self.selected = (r, c)
        self.hints_used += 1
        self._msg(f"Hint placed ({self.hints_used} used)", C_WARN)
        if self._complete(): self._finish()

    def solve_all(self):
        if self.board is None: return
        self.board = copy.deepcopy(self.initial)
        solve(self.board)
        self.done = True
        self.hint_cell = self.selected = None
        self._msg("Puzzle solved!", C_OK)

    def _complete(self):
        return all(
            self.board[r][c] != 0 and is_valid(self.board, self.board[r][c], r, c)
            for r in range(9) for c in range(9)
        )

    def _finish(self):
        self.done = True
        h = f"{self.hints_used} hint{'s' if self.hints_used!=1 else ''} used" if self.hints_used else "No hints used"
        self._msg(f"Solved!  ·  {h}", C_OK)

    def draw(self):
        self.screen.fill(BG)
        t = self.f_title.render("Sudoku", True, BLACK)
        self.screen.blit(t, t.get_rect(center=(WIN_W//2, 34)))
        for b in self.diff_btns: b.draw(self.screen, self.f_btn)
        if self.board is None:
            ph = self.f_msg.render("Select a difficulty and press New Game", True, GRAY_MID)
            self.screen.blit(ph, ph.get_rect(center=(WIN_W//2, BOARD_Y + GRID_PX//2)))
            for b in self.act_btns: b.draw(self.screen, self.f_btn)
            pygame.display.flip()
            return
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, GRID_PX, GRID_PX)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        sr, sc = self.selected if self.selected else (-1, -1)
        sn = self.board[sr][sc] if self.selected else 0
        for r in range(9):
            for c in range(9):
                x = BOARD_X + c * CELL
                y = BOARD_Y + r * CELL
                if self.selected and r == sr and c == sc:
                    bg = C_SEL
                elif self.selected:
                    if r==sr or c==sc or (r//3==sr//3 and c//3==sc//3):
                        bg = C_HL
                    elif sn and self.board[r][c] == sn:
                        bg = C_SAME
                    else:
                        bg = WHITE
                else:
                    bg = WHITE
                if bg != WHITE:
                    pygame.draw.rect(self.screen, bg, (x, y, CELL, CELL))
                num = self.board[r][c]
                if num:
                    if   self.hint_cell == (r, c):            col = C_HINT
                    elif self.initial[r][c]:                  col = C_FIXED
                    elif not is_valid(self.board, num, r, c): col = C_ERROR
                    else:                                     col = C_USER
                    s = self.f_cell.render(str(num), True, col)
                    self.screen.blit(s, s.get_rect(center=(x+CELL//2, y+CELL//2)))
        for i in range(10):
            lw  = 3 if i % 3 == 0 else 1
            lcl = BORDER if i % 3 == 0 else GRAY_LINE
            pygame.draw.line(self.screen, lcl, (BOARD_X, BOARD_Y+i*CELL), (BOARD_X+GRID_PX, BOARD_Y+i*CELL), lw)
            pygame.draw.line(self.screen, lcl, (BOARD_X+i*CELL, BOARD_Y), (BOARD_X+i*CELL, BOARD_BOTTOM), lw)
        for b in self.act_btns: b.draw(self.screen, self.f_btn)
        if self.msg:
            ms = self.f_msg.render(self.msg, True, self.msg_col)
            self.screen.blit(ms, ms.get_rect(center=(WIN_W//2, BOARD_BOTTOM + 64)))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                for b in self.all_btns: b.hovered = b.hit(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for b in self.diff_btns:
                    if b.hit(pos):
                        self._set_diff(b)
                        self._msg(f"{self.difficulty.capitalize()} — press New Game to start")
                if self.btn_new.hit(pos):   self.new_game()
                if self.btn_erase.hit(pos): self.erase()
                if self.btn_hint.hit(pos):  self.hint()
                if self.btn_solve.hit(pos): self.solve_all()
                bx, by = pos[0]-BOARD_X, pos[1]-BOARD_Y
                if self.board and 0<=bx<GRID_PX and 0<=by<GRID_PX and not self.done:
                    col, row = bx//CELL, by//CELL
                    if self.initial[row][col]:
                        self._msg("Fixed cell", C_ERR)
                        self.selected = None
                    else:
                        self.selected = (row, col)
                        self._msg("")
            if event.type == pygame.KEYDOWN:
                k = event.key
                if pygame.K_1 <= k <= pygame.K_9:               self.enter_num(k - pygame.K_0)
                elif k in (pygame.K_BACKSPACE, pygame.K_DELETE): self.erase()
                elif k == pygame.K_h:                            self.hint()
                elif k == pygame.K_s:                            self.solve_all()
                elif k == pygame.K_n:                            self.new_game()

        return True

async def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        running = game.handle_events()
        game.draw()
        await asyncio.sleep(0)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        from js import document, window
        js_code = """
        var inp = document.createElement('input');
        inp.type = 'text';
        inp.inputMode = 'numeric';
        inp.pattern = '[0-9]*';
        inp.style.cssText = 'position:fixed;opacity:0;width:1px;height:1px;top:0;left:0;border:none;outline:none;';
        inp.id = 'sudoku-input';
        document.body.appendChild(inp);
        document.addEventListener('click', function() {
            document.getElementById('sudoku-input').focus();
        });
        document.addEventListener('touchend', function() {
            document.getElementById('sudoku-input').focus();
        });
        document.getElementById('sudoku-input').addEventListener('input', function(e) {
            var val = this.value.replace(/[^1-9]/g, '');
            if (val.length > 0) {
                var digit = val[val.length - 1];
                var event = new KeyboardEvent('keydown', {
                    key: digit,
                    keyCode: 48 + parseInt(digit),
                    which: 48 + parseInt(digit),
                    bubbles: true
                });
                window.dispatchEvent(event);
            }
            this.value = '';
        });
        setTimeout(function() {
            document.getElementById('sudoku-input').focus();
        }, 1000);
        """
        window.eval(js_code)

    asyncio.run(main())
