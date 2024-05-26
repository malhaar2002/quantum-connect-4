Quantum computing concepts can be abstract and difficult to grasp for newcomers. This project seeks to create an accessible entry point into the world of quantum mechanics through a gamified version of Connect 4.

### Installation
To setup the game, start by cloning our repository. Install the dependencies by running `pip install -r requirements.txt`. To play the game on different computers over the same network, change the `SERVER_IP` variable in `constants.py` to your local IPv4 address. You can then start the server by running `python3 server.py`. In a separate terminal, run `python3 client.py` to launch the GUI. After both player run `client.py`, they are connected to the server and the game starts. If you want to try the game on CLI mode instead, run the `project_code.ipynb` file. 

### Objective
The goal of Quantum Connect 4 is to be the first player to connect four of your coins
horizontally, vertically, or diagonally on a 6x6 grid.
### Game Setup
Players:
- Player 0: Red
- Player 1: Yellow
Initial Board:
- The bottom row is initialized with alternating red and yellow coins to ensure no bias.
### How to Play
1. Turns:
- Players take turns, choosing to either place a coin in a column or play a gate secretly.
- If a player places a coin, the game board is updated instantly.
- If a player plays a gate, nothing is updated immediately (except when the swap gate is applied).
2. Gates:
- Each player has a limited number of gates.
Number of Gates per Player
- NOT Gate: 2
- Hadamard Gate: 1
- Swap Gate: 1
- CNOT Gate: 1
- Noise Gate: 1

### Gate Rules
1. NOT Gate:
- Flips the opponent’s piece to the player’s coin upon the next move in the specified
column.
- Applied to the first empty slot in the chosen column.
- The opponent will not know which gate is applied or where.
2. Hadamard Gate:
- Introduces a probabilistic element where the opponent’s piece can either become the
player’s or remain the opponent’s on the next move in the chosen column.
- Applied to the first empty slot in the chosen column.
- The opponent will not know which gate is applied or where.
3. CNOT Gate:
- Player chooses two columns (control and target).
- If the control column’s topmost filled coin is a 1 (yellow), placing a coin in the target
column will flip it.
4. Swap Gate:
- Allows players to swap the positions of one of their coins with one of the opponent’s.
The chosen coins can only be the topmost ones of any column
- The opponent will see the game board update instantaneously
5. Noise Gate:
- Causes the opponent’s coin to be placed randomly in any column during their turn.
Win Conditions
1. Four in a Row:
- Connect four of your coins horizontally, vertically, or diagonally to win.
2. Draw:
- The game ends in a draw if the board is completely filled without any player con-
necting four coins.

*To get a deeper understanding of how our quantum backend works, please go through example_game.ipynb*

# References
1. <a href='https://fullstackquantumcomputation.tech/blog/post-tutorial-QonnectFour/'> Qonnect four - Making a quantum game
2. https://github.com/ToJen/quantum-connect-four
3. https://www.techwithtim.net/tutorials/python-programming/python-online-game-tutorial
