BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PALE_TURQUOISE = (175, 238, 238)

SQUARESIZE = 80  # Adjusted size for smaller screen
RADIUS = int(SQUARESIZE / 2 - 10)
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

# Do not change unless you modified game.py accordingly
ROW_COUNT = 6
COLUMN_COUNT = 6

# Gates button locations
BOARD_WIDTH = COLUMN_COUNT * SQUARESIZE
BUTTON_BG_COLOR = PALE_TURQUOISE 
BUTTON_TEXT_COLOR = BLACK
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
NOT_GATE_1 = (BOARD_WIDTH + 50, 90)
NOT_GATE_2 = (BOARD_WIDTH + 50, 160)
HADAMARD_GATE_1 = (BOARD_WIDTH + 50, 230)
HADAMARD_GATE_2 = (BOARD_WIDTH + 50, 300)
SWAP_GATE = (BOARD_WIDTH + 50, 370)
CNOT_GATE = (BOARD_WIDTH + 50, 440)
NOISE = (BOARD_WIDTH + 50, 510)
