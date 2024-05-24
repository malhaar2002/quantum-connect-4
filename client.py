import pygame
from network import Network
import numpy as np
import sys
import math
import time
from constants import *

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

def create_button(screen, x, y, width, height, text, text_color, button_color):
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = pygame.font.SysFont("monospace", 18).render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)
    return text_rect

def choose_1qubit_gate(screen, n, game, gate_name, gate_symbol):
    label = pygame.font.SysFont("monospace", 30).render(f"Choose column to apply {gate_name}", 1, RED)
    screen.blit(label, (40,10))
    pygame.display.update()
    chosen_column = False
    while not chosen_column:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                if posx < BOARD_WIDTH - RADIUS:
                    col = int(math.floor(posx/SQUARESIZE))
                    chosen_column = True
                    n.send(f"{game.current_player},{col},{gate_symbol}")
                    print(f"{gate_name} applied")
                    break

def choose_2qubit_gate(screen, n, game, gate_name, gate_symbol):
    col1, col2 = None, None
    chosen_column_1, chosen_column_2 = False, False
    label = pygame.font.SysFont("monospace", 30).render(f"Choose Column 1 for {gate_name}", 1, RED)
    screen.blit(label, (40,10))
    pygame.display.update()
    while not chosen_column_1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                if posx < BOARD_WIDTH - RADIUS:
                    col1 = int(math.floor(posx/SQUARESIZE))
                    chosen_column_1 = True
                    break
    pygame.draw.rect(screen, BLACK, (0,0, BOARD_WIDTH, SQUARESIZE))
    label = pygame.font.SysFont("monospace", 30).render(f"Choose Column 2 for {gate_name}", 1, RED)
    screen.blit(label, (40,10))
    pygame.display.update()
    while not chosen_column_2:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                if posx < BOARD_WIDTH - RADIUS:
                    col2 = int(math.floor(posx/SQUARESIZE))
                    chosen_column_2 = True
                    break
    n.send(f"{game.current_player},{col1},{col2},{gate_symbol}")
    print(f"Swap Gate applied")

def main():
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    window_width = BOARD_WIDTH * 1.5
    height = (ROW_COUNT+1) * SQUARESIZE
    size = (window_width, height)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quantum Connect Four")
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 30)

    # create gate buttons
    not_gate_1 = create_button(screen, NOT_GATE_1[0], NOT_GATE_1[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Not Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    not_gate_2 = create_button(screen, NOT_GATE_2[0], NOT_GATE_2[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Not Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    hadamard_gate_1 = create_button(screen, HADAMARD_GATE_1[0], HADAMARD_GATE_1[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Hadamard Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    hadamard_gate_2 = create_button(screen, HADAMARD_GATE_2[0], HADAMARD_GATE_2[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Hadamard Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    swap_gate = create_button(screen, SWAP_GATE[0], SWAP_GATE[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Swap Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    cnot_gate = create_button(screen, CNOT_GATE[0], CNOT_GATE[1], BUTTON_WIDTH, BUTTON_HEIGHT, "CNOT Gate", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
    noise_gate = create_button(screen, NOISE[0], NOISE[1], BUTTON_WIDTH, BUTTON_HEIGHT, "Noise", BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)

    while not game_over:

        try:
            game = n.send("get")
        except Exception as e:
            game_over = True
            print("Couldn't get game")
            print("Error:", e)
            break

        # check win condition
        if game.win_condition():
            n.send("reset")
            if game.current_player == 0:
                label = myfont.render(f"Yellow wins!", 1, RED)
            elif game.current_player == 1:
                label = myfont.render(f"Red wins!", 1, RED)
            screen.blit(label, (40,10))
            pygame.display.update()
            game_over = True

        # check draw condition
        elif np.all(board != -1):
            n.send("reset")
            label = myfont.render(f"It's a Draw", 1, RED)
            screen.blit(label, (40,10))
            pygame.display.update()
            game_over = True

        draw_board(np.flip(game.board, 0), screen, SQUARESIZE, RADIUS, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pygame.draw.rect(screen, BLACK, (0,0, window_width, SQUARESIZE))
            if event.type == pygame.MOUSEMOTION and event.pos[0] < BOARD_WIDTH - RADIUS:
                posx = event.pos[0]
                if game.current_player == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                pygame.draw.rect(screen, BLACK, (0,0, BOARD_WIDTH, SQUARESIZE))

                if game.current_player == player:
                    posx = event.pos[0]
                    if posx < BOARD_WIDTH - RADIUS:
                        # clicked on the game board
                        col = int(math.floor(posx/SQUARESIZE))
                        n.send(f"{game.current_player},{col},P")
                        board = np.flip(game.board, 0)
                        print_board(board)
                        draw_board(board, screen, SQUARESIZE, RADIUS, height)
                    elif not_gate_1.collidepoint(event.pos):
                        choose_1qubit_gate(screen, n, game, "Not Gate", "X")
                        pygame.draw.rect(screen, BLACK, (NOT_GATE_1[0], NOT_GATE_1[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif not_gate_2.collidepoint(event.pos):
                        choose_1qubit_gate(screen, n, game, "Not Gate", "X")
                        pygame.draw.rect(screen, BLACK, (NOT_GATE_2[0], NOT_GATE_2[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif hadamard_gate_1.collidepoint(event.pos):
                        choose_1qubit_gate(screen, n, game, "Hadamard Gate", "H")
                        pygame.draw.rect(screen, BLACK, (HADAMARD_GATE_1[0], HADAMARD_GATE_1[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif hadamard_gate_2.collidepoint(event.pos):
                        choose_1qubit_gate(screen, n, game, "Hadamard Gate", "H")
                        pygame.draw.rect(screen, BLACK, (HADAMARD_GATE_2[0], HADAMARD_GATE_2[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif cnot_gate.collidepoint(event.pos):
                        choose_2qubit_gate(screen, n, game, "CNOT Gate", "C")
                        pygame.draw.rect(screen, BLACK, (CNOT_GATE[0], CNOT_GATE[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif swap_gate.collidepoint(event.pos):
                        choose_2qubit_gate(screen, n, game, "Swap Gate", "S")
                        pygame.draw.rect(screen, BLACK, (SWAP_GATE[0], SWAP_GATE[1], BUTTON_WIDTH, BUTTON_HEIGHT))
                    elif noise_gate.collidepoint(event.pos):
                        n.send(f"{game.current_player},-1,N")
                        print("Noise applied")
                        pygame.draw.rect(screen, BLACK, (NOISE[0], NOISE[1], BUTTON_WIDTH, BUTTON_HEIGHT))

                if game_over:
                    pygame.time.wait(1000)

    time.sleep(3)
    return game_over

if __name__ == "__main__":
    main()