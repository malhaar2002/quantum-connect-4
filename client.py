import pygame
from network import Network
import pickle
import numpy as np
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 4
COLUMN_COUNT = 4

def create_board():
    board = np.full((ROW_COUNT,COLUMN_COUNT), -1)
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def print_board(board):
    print(np.flip(board, 0))

def draw_board(board, screen, SQUARESIZE, RADIUS, height):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 0:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def main():
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        try:
            game = n.send("get")
        except Exception as e:
            game_over = True
            print("Couldn't get game")
            print("Error:", e)
            break

        draw_board(np.flip(game.board, 0), screen, SQUARESIZE, RADIUS, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if game.current_player == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                if game.current_player == player:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    # send to server
                    n.send(f"{game.current_player}, {col}")
                    board = np.flip(game.board, 0)

                    if game.win_condition():
                        label = myfont.render(f"Player {game.current_player} wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    print_board(board)
                    draw_board(board, screen, SQUARESIZE, RADIUS, height)

                if game_over:
                    pygame.time.wait(3000)

if __name__ == "__main__":
    main()