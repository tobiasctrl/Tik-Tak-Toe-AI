import pygame


class MiniMax:
    def __init__(self, GameBoard):
        self.GameBoard = GameBoard

    def evaluate(self):
        # 1 = x won
        # 0 = tie
        # -1 = o won
        for row in range(3):
            if self.GameBoard[row][0] == self.GameBoard[row][1] and self.GameBoard[row][1] == self.GameBoard[row][2]:
                if self.GameBoard[row][0] == 'x':
                    return 1
                elif self.GameBoard[row][0] == 'o':
                    return -1
        for col in range(3):
            if self.GameBoard[0][col] == self.GameBoard[1][col] and self.GameBoard[1][col] == self.GameBoard[2][col]:
                if self.GameBoard[0][col] == 'x':
                    return 1
                elif self.GameBoard[0][col] == 'o':
                    return -1
        if self.GameBoard[0][0] == self.GameBoard[1][1] and self.GameBoard[2][2] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        if self.GameBoard[0][2] == self.GameBoard[1][1] and self.GameBoard[2][0] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        for i in range(3):
            for j in range(3):
                if self.GameBoard[i][j] == '-':
                    return 2
        return 0

    def max(self):
        x = None
        y = None
        max_eval = -2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'x'
                    min_eval = self.min()[0]
                    if max_eval < min_eval:
                        max_eval = min_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return(max_eval, x, y)

    def min(self):
        x = None
        y = None
        min_eval = 2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'o'
                    max_eval = self.max()[0]
                    if min_eval > max_eval:
                        min_eval = max_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return(min_eval, x, y)


class GameLoop:
    def __init__(self):
        self.GameState = 2
        background_color = (0, 0, 0)
        self.foreground_color = (255, 255, 255)
        (width, height) = (600, 600)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Tik Tak Toe AI')
        self.screen.fill(background_color)
        pygame.display.flip()

    def RenderUI(self, gameboard):
        self.gameboard = gameboard

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    x = round(Mouse_x/200 - 0.49)
                    y = round(Mouse_y/200 - 0.49)
                    self.GameOver()
                    if self.GameState == 2:
                        ValidMove = self.MakeMove(x, y, 'o')
                        if ValidMove:
                            return self.gameboard
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.DrawBoard()
            for row in range(3):
                for col in range(3):
                    if self.gameboard[row][col] == 'x':
                        self.DrawX(col, row)
                    if self.gameboard[row][col] == 'o':
                        self.DrawO(col, row)
            pygame.display.update()

    def DrawBoard(self):
        '''Draws the lines of the GameBoard'''
        for xy in range(200, 401, 200):
            pygame.draw.line(self.screen, self.foreground_color,
                             (0, xy), (600, xy), 3)
            pygame.draw.line(self.screen, self.foreground_color,
                             (xy, 0), (xy, 600), 3)

    def DrawX(self, x, y):
        x += 1
        y += 1
        pygame.draw.line(self.screen, self.foreground_color, (200 * x -
                                                              200 + 10, 200 * y - 200 + 10), ((x * 200) - 10, (y * 200) - 10), 3)
        pygame.draw.line(self.screen, self.foreground_color, (200 * x - 200 + 10,
                                                              (y * 200) - 10), ((x * 200) - 10, 200 * y - 200 + 10), 3)

    def DrawO(self, x, y):
        x += 1
        y += 1
        pygame.draw.circle(self.screen, self.foreground_color,
                           (x * 200 - 100, y * 200 - 100), 90, 3)

    def MakeMove(self, x, y, player):

        if self.gameboard[y][x] == '-':
            self.gameboard[y][x] = player
            return True
        return False

    def GameOver(self):
        self.GameState = MiniMax(self.gameboard).evaluate()
        if self.GameState == 1:
            print('x Won this Game')
        elif self.GameState == 0:
            print('None Won')
        elif self.GameState == -1:
            print('o Won this Game')


if __name__ == "__main__":
    Board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    GL = GameLoop()
    while True:
        GL.RenderUI(Board)
        MM = MiniMax(Board)
        bestmove = MM.max()
        GL.MakeMove(bestmove[1], bestmove[2], 'x')