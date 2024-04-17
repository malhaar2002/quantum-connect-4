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
        self.board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
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
        for c in range(self, self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self, self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self, self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):		
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif board[r][c] == 2: 
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()

    def run(self):
        board = create_board()
        print_board(board)
        game_over = False
        turn = 0

        pygame.init()

        SQUARESIZE = 100

        width = COLUMN_COUNT * SQUARESIZE
        height = (ROW_COUNT+1) * SQUARESIZE

        size = (width, height)

        RADIUS = int(SQUARESIZE/2 - 5)

        screen = pygame.display.set_mode(size)
        draw_board(board)
        pygame.display.update()

        myfont = pygame.font.SysFont("monospace", 75)

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if winning_move(board, 1):
                                label = myfont.render("Player 1 wins!!", 1, RED)
                                screen.blit(label, (40,10))
                                game_over = True


                    # # Ask for Player 2 Input
                    else:				
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            if winning_move(board, 2):
                                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                                screen.blit(label, (40,10))
                                game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        pygame.time.wait(3000)

