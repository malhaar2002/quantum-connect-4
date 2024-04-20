import numpy as np
import pygame
import sys
import math
# from project_code import QuantumGameInteractive

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# game = QuantumGameInteractive()

# Add the quantum gates and their counts for each player
player_gates = {0: {"NOT": 2, "HADAMARD": 2, "SWAP": 2, "ROTATION": 2},
                1: {"NOT": 2, "HADAMARD": 2, "SWAP": 2, "ROTATION": 2}}

def create_board():
	# board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	# Initialise the board with -1
	board = np.full((ROW_COUNT,COLUMN_COUNT), -1)
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece
	# board = game.update_board(piece, col, 'P')


def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == -1

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == -1:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
			
def draw_board(board):
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

def draw_buttons():	
	button_surface = pygame.Surface((50, 50))
	
	text = myfont.render("NOT", True, (0, 0, 0))
	text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))

	button_rect = pygame.Rect(125, 125, 50, 50)

	return button_rect

    #button_margin = 10
	#button_width = 100
    #button_height = 50

    #button_positions = [
    #    (width - button_width - button_margin, button_margin),
    #    (width - button_width - button_margin, button_margin + button_height + button_margin),
    #    (width - button_width - button_margin, button_margin + 2*(button_height + button_margin)),
    #    (width - button_width - button_margin, button_margin + 3*(button_height + button_margin))
    #]

    #button_texts = ["Button 1", "Button 2", "Button 3", "Button 4"]

    #for i, (x, y) in enumerate(button_positions):
    #    pygame.draw.rect(screen, RED, (x, y, button_width, button_height))
    #    button_text = myfont.render(button_texts[i], True, BLACK)
    #    screen.blit(button_text, (x + 10, y + 10))

    #pygame.display.update()

def handle_click(pos):
    button_margin = 10
    button_width = 100
    button_height = 50

    button_positions = [
        (width - button_width - button_margin, button_margin),
        (width - button_width - button_margin, button_margin + button_height + button_margin),
        (width - button_width - button_margin, button_margin + 2*(button_height + button_margin)),
        (width - button_width - button_margin, button_margin + 3*(button_height + button_margin))
    ]

    for i, (x, y) in enumerate(button_positions):
        if x <= pos[0] <= x + button_width and y <= pos[1] <= y + button_height:
            print(f"Button {i+1} clicked!")


board = create_board()
print_board(board)
game_over = False
turn = 0
# game = project_code.QuantumGameInteractive()

pygame.init()

SQUARESIZE = 90

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width+5, height+5)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

draw_board(board)
draw_buttons()
pygame.display.update()


while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = pygame.mouse.get_pos()
			handle_click(pos)

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

		# Draw the buttons for quantum gates
		# draw_buttons()
		pygame.display.update()
		# pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 0)

					if winning_move(board, 0):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True
					elif np.all(board != -1):
						label = myfont.render("It's a draw!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True


			# # Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 2 wins!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True
					elif np.all(board != -1):
						label = myfont.render("It's a draw!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)