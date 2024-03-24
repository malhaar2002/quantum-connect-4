Quantum computing concepts can be abstract and difficult to grasp for newcomers. This project seeks to create an accessible entry point into the world of quantum mechanics through a gamified version of Connect 4.

# Rules
Unlike traditional Connect 4, where the objective is simply to connect four of one's own pieces in a line, Quantum Connect 4 adds a layer of strategic depth and unpredictability by granting players special quantum gate cards. Each player will get a fixed number of gate cards that can be used anytime during the game. The gates can only be applied on the first empty grid above the filled columns. They equip the player with unique abilities to alter the state of the game board by manipulating the pieces in ways that mimic quantum operations. Here are the rules of applying different gate cards on the game board: 
- Not gate: Flips the opponent's piece to the player's coin upon the next move. 
- Hadamard Gate: This gate introduces a probabilistic element, where the opponent's piece can either become the player's or remain the opponent's on the following move. The concept mirrors the quantum superposition principle. Both players are informed when and where the Hadamard Gate will be applied. After its application, the player has two options: measuring the gate or applying a CNOT gate on top of it, transforming it into an entangled state. 
- CNOT gate: Entangles two selected positions on the board, such that a change in one will mirror in the other, showcasing quantum entanglement. 
- Swap gate: This gate enables players to swap the positions of one of their game pieces with one belonging to their opponent. Following the application of this gate, measurements will be taken of both qubits.
- Rotation gate: In the game, instead of employing the quantum rotation gate that alters the angle across the Bloch sphere without changing the measurement, we implemented a similar approach. In this approach, we play the Player's coin that would have been on the ith qubit on the n-ith qubit, changing the opponent's chosen slot from i to n-i.


*To go through an example gameplay, please go through example_game.ipynb*

# References
1. Qonnect four - Making a quantum game
2. https://github.com/ToJen/quantum-connect-four
