
from qiskit import QuantumCircuit, Aer, execute
from qiskit import *
import numpy as np
import matplotlib

class QuantumGameInteractive:
    def __init__(self):
        self.board = np.full((4, 4), -1)  # Initialize the board
        self.board[3] = [0, 1, 0, 1]  # Initial configuration
        self.qr = QuantumRegister(4)
        self.cr = ClassicalRegister(4)
        self.qc = QuantumCircuit(self.qr, self.cr)
        # self.qc = QuantumCircuit(4, 4)  
        self.secret_x_pending = [0] * 4  # Track pending secret X gates
        self.state_before_hgate = [-1] * 4
        self.h_flag = [0] * 4
        self.r_flag = 0

        # Apply initial X gates based on the board's configuration
        for qubit in range(4):
            if self.board[3][qubit] == 1:
                self.qc.x(qubit)

    def apply_pending_secret_x(self, qubit):
        while self.secret_x_pending[qubit] > 0:
            self.qc.x(qubit)
            self.secret_x_pending[qubit] -= 1

    def measure_qubit(self, qubit):
        self.apply_pending_secret_x(qubit)  # Apply pending X before measurement

        temp_qc = self.qc.copy()
        temp_qc.measure(qubit, qubit)
        backend = Aer.get_backend('qasm_simulator')
        job = execute(temp_qc, backend, shots=1)
        result = job.result()
        counts = result.get_counts(temp_qc)
        measured_value = int(list(counts.keys())[0][3 - qubit])
        return measured_value

    def update_board(self, player, qubit, action):
        if action == 'X':
            # Mark a secret X gate for future application
            self.secret_x_pending[qubit] += 1
            return  
        
        if action == 'H':
            self.h_flag[qubit] +=1
            self.state_before_hgate[qubit] = self.measure_qubit(qubit) 
            self.qc.h(qubit)
            print(f"Player {player} played Hadamard gate on {qubit}:")
            return 
        
        if action == 'S':
            self.qc.swap(self.qr[qubit[0]], self.qr[qubit[1]])
            # Update value of first qubit after swapping
            measured_value = self.measure_qubit(qubit[0])
            for row in reversed(range(4)):
                if self.board[row][qubit[0]] == -1:
                    self.board[row+1][qubit[0]] = measured_value
                    break
            # Update value of second qubit after swapping
            measured_value = self.measure_qubit(qubit[1])
            for row in reversed(range(4)):
                if self.board[row][qubit[1]] == -1:
                    self.board[row+1][qubit[1]] = measured_value
                    break
            print(f"Player {player} updated the board")
            print(self.board)
            return
        
        if action == 'R':
            self.r_flag +=1
            return

        # Desired outcome aligns with the player's identity (0 or 1)
        desired_outcome = player

        # If there is rotation flag, change the qubit of the player
        if self.r_flag:
            qubit = 3 - qubit
            self.r_flag -=1

        if self.secret_x_pending[qubit]== 0:
            # Measured when no  X gate applied on the qubit. 
            current_state = self.measure_qubit(qubit) 
        elif self.state_before_hgate[qubit]==0 or self.state_before_hgate[qubit]==1:
            current_state= self.state_before_hgate[qubit]
            self.state_before_hgate[qubit] = -1
        else:
            # We only want to measure if there is no X gate applied to that qubit. But if there is 1, we reverse the qubit being measured because the other player when playing their turn won't havre an idea of the X gate. 
            current_state = self.measure_qubit(qubit)
            # print(self.secret_x_pending[qubit])
            current_state = 1- current_state
        
        if current_state != desired_outcome:
            self.qc.x(qubit)  # Apply an X gate to achieve desired outcome

        if self.h_flag[qubit] ==0:
            measured_value = self.measure_qubit(qubit)  # Measure after adjustments
        else:
            # initialising value after Hadamard gate
            measured_value = self.measure_qubit(qubit)
            self.h_flag[qubit] -=1
            if measured_value ==1:
                self.qc.initialize([0, 1], qubit)
            else:
                self.qc.initialize([1, 0], qubit)

        # Update the board in the lowest available row for the qubit
        for row in reversed(range(4)):
            if self.board[row][qubit] == -1:
                self.board[row][qubit] = measured_value
                break
        print(f"Player {player} updated the board:")

        print(self.board)
        return self.board
    
    def win_condition(self):
        # Check for a win condition
        for row in range(4):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.board[row][3] != -1:
                return True

        for col in range(4):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.board[3][col] != -1:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] != -1:
            return True

        if self.board[0][3] == self.board[1][2] == self.board[2][1] == self.board[3][0] != -1:
            return True

        return False

    def play_game(self):
        current_player = 0
        while True:
            print(f"\nPlayer {current_player}'s turn.")
            qubit = int(input("Choose a qubit to interact with (0-3): "))
            action = input("Type 'X' for X gate, 'H' for H gate, 'S' for Swap gate, 'R' for Rotation gate or 'P' to measure and place: ").upper()
            if action == 'S':
                other_qubit = int(input("Choose the other qubit to swap the First qubit with:"))
                qubit = [qubit, other_qubit]

            self.update_board(current_player, qubit, action)

            if self.win_condition():
                print(f"Player {current_player} wins!")
                break
            elif np.all(self.board != -1):
                print("It's a draw!")
                break

            # We will Implement win condition check and full board check here

            # Switch to the next player
            current_player = 1 - current_player

game = QuantumGameInteractive()
game.play_game()




