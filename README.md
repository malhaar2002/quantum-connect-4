Quantum computing concepts can be abstract and difficult to grasp for newcomers. This project seeks to create an accessible entry point into the world of quantum mechanics through a gamified version of Connect 4.

## Installation
Follow these steps to set up and play Quantum Connect 4:

1. **Clone the Repository**
    ```sh
    git clone https://github.com/malhaar2002/quantum-connect-4.git
    cd quantum-connect-4
    ```

2. **Create a Virtual Environment** <br>
    We recommend creating a virtual environment to avoid any conflicts with existing packages. You can do this using the `venv` module:

    - On Windows:
        ```sh
        python -m venv env
        .\env\Scripts\activate
        ```

    - On macOS and Linux:
        ```sh
        python3 -m venv env
        source env/bin/activate
        ```

3. **Install Dependencies** <br>
    Install the required dependencies by running:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure Server IP** <br>
    To play the game on different computers over the same network, update the `SERVER_IP` variable in `constants.py` to your local IPv4 address. For playing on the same computer, you can leave it as `127.0.0.1` (localhost).

5. **Start the Server** <br>
    Start the server by running:
    ```sh
    python3 server.py
    ```

6. **Launch the Game Clients** <br>
    Each player should launch the game client. To do this, run the following command on both computers:
    ```sh
    python3 client.py
    ```

    This will start the game GUI for each player.

7. **Playing on a Single Computer** <br>
    If you want to play the game on a single computer, simply run `client.py` in two separate terminals
    Both players will then be connected to the server, and the game will start.

8. **Optional: Try CLI Mode**
    To get a broad understanding of how the quantum gates work, you can try the game in CLI mode by running the Jupyter notebook `project_code.ipynb`:

You are now ready to play Quantum Connect 4!

## Objective
The goal of Quantum Connect 4 is to be the first player to connect four of your coins horizontally, vertically, or diagonally on a 6x6 grid.

## Game Setup
Players:
- Player 0: Red
- Player 1: Yellow

Initial Board:
- The bottom row is initialized with alternating red and yellow coins to ensure no bias.

## How to Play
1. **Turns**:
    - Players take turns, choosing to either place a coin in a column or play a gate secretly.
    - If a player places a coin, the game board is updated instantly.
    - If a player plays a gate, nothing is updated immediately (except for the swap gate).

2. **Gates**:
    - Each player has a limited number of gates:
        - NOT Gate: 2
        - Hadamard Gate: 1
        - Swap Gate: 1
        - CNOT Gate: 1
        - Noise Gate: 1

## Gate Rules
1. **NOT Gate**:
    - Flips the opponent’s piece to the player’s coin upon the next move in the specified column.
    - Applied to the first empty slot in the chosen column.
    - The opponent will not know which gate is applied or where.

2. **Hadamard Gate**:
    - Introduces a probabilistic element where the opponent’s piece can either become the player’s or remain the opponent’s on the next move in the chosen column.
    - Applied to the first empty slot in the chosen column.
    - The opponent will not know which gate is applied or where.

3. **CNOT Gate**:
    - Player chooses two columns (control and target).
    - If the control column’s topmost filled coin is a 1 (yellow), placing a coin in the target column will flip it.

4. **Swap Gate**:
    - Allows players to swap the positions of one of their coins with one of the opponent’s.
    - The chosen coins can only be the topmost ones of any column.
    - The opponent will see the game board update instantaneously.

5. **Noise Gate**:
    - Causes the opponent’s coin to be placed randomly in any column during their turn.

## Win Conditions
1. **Four in a Row**:
    - Connect four of your coins horizontally, vertically, or diagonally to win.

2. **Draw**:
    - The game ends in a draw if the board is completely filled without any player connecting four coins.

## How the Game Works

Each column of the game board is represented as a qubit in our quantum circuit, resulting in a circuit with 6 qubits. Here's a brief explanation of how the game operates:

### Game Board and Circuit
- **Qubits and Columns**: Each column corresponds to a qubit, and the state of each column is represented by the qubit's state.
- **6x6 Matrix**: The game board is maintained through a 6x6 matrix. Each element of the matrix represents a position on the board and is updated based on the measurement of the corresponding qubit.
- **Measurement**: At any point when the circuit is measured, the result determines the coins placed at the topmost row of each column.

### Player Actions and Gate Implementations

Players can perform various actions, represented by applying quantum gates to the qubits. Here’s how each action is implemented:

1. **X - NOT Gate**:
    - **Description**: Flips the state of the qubit (0 to 1 and vice versa).
    - **Implementation**: Increment a counter for delayed application to the qubit.

2. **H - Hadamard Gate**:
    - **Description**: Creates a superposition state, changing the probability of the qubit being in 0 or 1.
    - **Implementation**: Measure the qubit, apply the Hadamard gate, and set a flag to indicate the change.

3. **S - Swap Gate**:
    - **Description**: Swaps the states of two qubits.
    - **Implementation**: Measure the qubit, swap the states, and update the game board immediately to reflect the change.

4. **N - Noise**:
    - **Description**: Simulates noise in the quantum circuit, affecting the state of the qubit.
    - **Implementation**: Increment a counter to apply noise in the next step.

5. **C - CNOT Gate**:
    - **Description**: A controlled-NOT gate, where one qubit (control) can flip the state of another qubit (target).
    - **Implementation**: Define the control and target qubit interaction and set a flag for the target qubit.

6. **P - Place Coin and Measure**:
    - **Description**: Measures the qubit and places a coin in the game board.
    - **Implementation**: Measure the qubit, possibly apply the X gate if needed, and place the resulting state in the lowest available row of the corresponding column.

*To get a deeper understanding of how our quantum backend works, please go through example_game.ipynb.*

### References
1. <a href='https://fullstackquantumcomputation.tech/blog/post-tutorial-QonnectFour/'> Qonnect four - Making a quantum game
2. https://github.com/ToJen/quantum-connect-four
3. https://www.techwithtim.net/tutorials/python-programming/python-online-game-tutorial
