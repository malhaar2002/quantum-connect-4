import numpy as np
import pygame
import sys
import math
from network import Network

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

class Game:
    def __init__(self):
        self.ROW_COUNT = 4
        self.COLUMN_COUNT = 4
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT+1) * self.SQUARESIZE
        self.board = np.full((self.ROW_COUNT,self.COLUMN_COUNT), -1)
        self.turn = 1
        self.run()

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == -1

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == -1:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def draw_board(self):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):		
                if self.board[r][c] == 0:
                    pygame.draw.circle(self.screen, RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif self.board[r][c] == 1: 
                    pygame.draw.circle(self.screen, YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()

    def run(self):
        self.print_board()
        game_over = False
        turn = 0

        pygame.init()

        size = (self.width, self.height)


        self.screen = pygame.display.set_mode(size)
        self.draw_board()
        pygame.display.update()

        myfont = pygame.font.SysFont("monospace", 75)

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(self.screen, RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                    else: 
                        pygame.draw.circle(self.screen, YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 0)

                            if self.winning_move(0):
                                label = myfont.render("Player 1 wins!!", 1, RED)
                                self.screen.blit(label, (40,10))
                                game_over = True


                    # # Ask for Player 2 Input
                    else:				
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 1)

                            if self.winning_move(1):
                                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                                self.screen.blit(label, (40,10))
                                game_over = True

                    self.print_board()
                    self.draw_board()

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        pygame.time.wait(3000)

game = Game()