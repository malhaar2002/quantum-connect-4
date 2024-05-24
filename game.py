from qiskit import QuantumCircuit, Aer, execute
from qiskit import *
import numpy as np
from constants import ROW_COUNT, COLUMN_COUNT

class Game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.current_player = 0
        self.board = np.full((ROW_COUNT, COLUMN_COUNT), -1)  # Initialize the board
        self.board[5] = [0, 1, 0, 1, 0, 1]  # Initial configuration
        self.qr = QuantumRegister(COLUMN_COUNT)  
        self.cr = ClassicalRegister(COLUMN_COUNT)
        self.qc = QuantumCircuit(self.qr, self.cr)
        # self.qc = QuantumCircuit(4, 4)  
        self.secret_x_pending = [0] * 6  # Track pending secret X gates
        self.state_before_hgate = [-1] * 6 # Storing measurement value before applying H gate
        self.h_flag = [0] * 6 # Tracking H gate for each qubit
        self.n_flag = 0 # Tracking Rotation gate for each qubit
        self.filled_column = [0]*6
        
        # Apply initial X gates based on the board's configuration
        for qubit in range(6):
            if self.board[5][qubit] == 1:
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
        measured_value = int(list(counts.keys())[0][5 - qubit])
        return measured_value

    def update_board(self, player, qubits, action):
        if action == 'X':
            # Mark a secret X gate for future application
            self.secret_x_pending[qubits] += 1
            self.current_player = 1 - self.current_player
            return  
        
        if action == 'H':
            self.h_flag[qubits] +=1 # Increment H flag value for that qubits
            self.state_before_hgate[qubits] = self.measure_qubit(qubits) # Before applying H gate stored qubits's measured value
            self.qc.h(qubits) # Applying H gate
            print(f"Player {player} played Hadamard gate on qubits {qubits}:")
            self.current_player = 1 - self.current_player
            return 
        
        if action == 'S':
            self.qc.swap(self.qr[qubits[0]], self.qr[qubits[1]])
            # Update value of first qubits after swapping
            measured_value = self.measure_qubit(qubits[0])
            for row in reversed(range(6)):
                if self.board[row][qubits[0]] == -1:
                    self.board[row+1][qubits[0]] = measured_value
                    break
            # Update value of second qubits after swapping
            measured_value = self.measure_qubit(qubits[1])
            for row in reversed(range(6)):
                if self.board[row][qubits[1]] == -1:
                    self.board[row+1][qubits[1]] = measured_value
                    break
            print(f"Player {player} updated the board")
            print(self.board)
            self.current_player = 1 - self.current_player
            return
        
        if action == 'N':
            self.n_flag +=1 # Incrementing flag value
            self.current_player = 1 - self.current_player
            return

        if action == 'C':
            control_qubit, target_qubit = qubits
            control_value = self.measure_qubit(control_qubit)
            if control_value == 1:
                for row in range(6):
                    if self.board[row][target_qubit] != -1:
                        self.board[row][target_qubit] = 1 - self.board[row][target_qubit]
                        break
            print(f"Player {player} applied CNOT gate with control qubit {control_qubit} and target qubit {target_qubit}")
            print(self.board)
            return

        # Desired outcome aligns with the player's identity (0 or 1)
        desired_outcome = player

        # If there is rotation flag, change the qubits of the player
        if self.n_flag:
            qubits = 5 - np.random.randint(6)
            self.n_flag -=1

        if self.secret_x_pending[qubits]== 0:
            # Measured when no  X gate applied on the qubits. 
            current_state = self.measure_qubit(qubits) 
            # If H gate has been applied to that qubits
        elif self.state_before_hgate[qubits]==0 or self.state_before_hgate[qubits]==1:
            current_state= self.state_before_hgate[qubits]
            self.state_before_hgate[qubits] = -1
        else:
            # We only want to measure if there is no X gate applied to that qubits. But if there is 1, we reverse the qubits being measured because the other player when playing their turn won't havre an idea of the X gate. 
            current_state = self.measure_qubit(qubits)
            # print(self.secret_x_pending[qubits])
            current_state = 1 - current_state
        
        if current_state != desired_outcome:
            self.qc.x(qubits)  # Apply an X gate to achieve desired outcome

        if self.h_flag[qubits] ==0:
            measured_value = self.measure_qubit(qubits)  # Measure after adjustments
        else:
            # initialising value after Hadamard gate
            measured_value = self.measure_qubit(qubits)
            self.h_flag[qubits] -=1
            # Initialising value once the qubits that had a Hadamard gate was measured to avoid any future discrepencies
            if measured_value == 1:
                self.qc.initialize([0, 1], qubits)
            else:
                self.qc.initialize([1, 0], qubits)

        # Update the board in the lowest available row for the qubits
        for row in reversed(range(6)):
            if self.board[row][qubits] == -1:
                self.board[row][qubits] = measured_value
                break
        print(f"Player {player} updated the board:")

        print(self.board)
        if self.board[0][qubits] != -1:
            self.filled_column[qubits] = 1
            
        self.current_player = 1 - self.current_player
        return self.board
    
    def win_condition(self):
        # Check horizontal lines for a win condition
        for row in range(6):  # there are 6 rows in a 6x6 board
            for col in range(3):  # up to the 3rd column to have space for four in a row
                if (self.board[row][col] == self.board[row][col + 1] ==
                    self.board[row][col + 2] == self.board[row][col + 3] != -1):
                    return True

        # Check vertical lines for a win condition
        for col in range(6):  # there are 6 columns in a 6x6 board
            for row in range(3):  # up to the 3rd row to have space for four in a row
                if (self.board[row][col] == self.board[row + 1][col] ==
                    self.board[row + 2][col] == self.board[row + 3][col] != -1):
                    return True

        # Check diagonal lines (down-right) for a win condition
        for row in range(3):  # up to the 3rd row to have space for diagonal four in a row
            for col in range(3):  # up to the 3rd column to have space for diagonal four in a row
                if (self.board[row][col] == self.board[row + 1][col + 1] ==
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != -1):
                    return True

        # Check diagonal lines (up-right) for a win condition
        for row in range(3, 6):  # start from the 4th row to the last to have space for diagonal four in a row
            for col in range(3):  # up to the 3rd column to have space for diagonal four in a row
                if (self.board[row][col] == self.board[row - 1][col + 1] ==
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3] != -1):
                    return True

        return False

# from qiskit import QuantumCircuit, Aer, execute
# from qiskit import *
# import numpy as np
# from constants import ROW_COUNT, COLUMN_COUNT

# class Game:
#     def __init__(self, id):
#         self.id = id
#         self.ready = False
#         self.current_player = 0
#         self.board = np.full((ROW_COUNT, COLUMN_COUNT), -1)  # Initialize the board
#         self.board[5] = [0, 1, 0, 1, 0, 1]  # Initial configuration
#         self.qr = QuantumRegister(COLUMN_COUNT)  
#         self.cr = ClassicalRegister(COLUMN_COUNT)
#         self.qc = QuantumCircuit(self.qr, self.cr)
#         # self.qc = QuantumCircuit(4, 4)  
#         self.secret_x_pending = [0] * 6  # Track pending secret X gates
#         self.state_before_hgate = [-1] * 6 # Storing measurement value before applying H gate
#         self.h_flag = [0] * 6 # Tracking H gate for each qubit
#         self.n_flag = 0 # Tracking Rotation gate for each qubit
#         self.filled_column = [0]*6
        
#         # Apply initial X gates based on the board's configuration
#         for qubit in range(6):
#             if self.board[5][qubit] == 1:
#                 self.qc.x(qubit)

#     def apply_pending_secret_x(self, qubit):
#         while self.secret_x_pending[qubit] > 0:
#             self.qc.x(qubit)
#             self.secret_x_pending[qubit] -= 1

#     def measure_qubit(self, qubit):
#         self.apply_pending_secret_x(qubit)  # Apply pending X before measurement

#         temp_qc = self.qc.copy()
#         temp_qc.measure(qubit, qubit)
#         backend = Aer.get_backend('qasm_simulator')
#         job = execute(temp_qc, backend, shots=1)
#         result = job.result()
#         counts = result.get_counts(temp_qc)
#         measured_value = int(list(counts.keys())[0][5 - qubit])
#         return measured_value

#     def update_board(self, player, qubit, action):
#         if action == 'X':
#             # Mark a secret X gate for future application
#             self.secret_x_pending[qubit] += 1
#             self.current_player = 1 - self.current_player
#             return  
        
#         if action == 'H':
#             print(f"Player {player} qubit {qubit} action {action}")
#             self.h_flag[qubit] +=1 # Increment H flag value for that qubit
#             self.state_before_hgate[qubit] = self.measure_qubit(qubit) # Before applying H gate stored qubit's measured value
#             self.qc.h(qubit) # Applying H gate
#             print(f"Player {player} played Hadamard gate on qubit {qubit}:")
#             self.current_player = 1 - self.current_player
#             return 
        
#         if action == 'S':
#             self.qc.swap(self.qr[qubit[0]], self.qr[qubit[1]])
#             # Update value of first qubit after swapping
#             measured_value = self.measure_qubit(qubit[0])
#             for row in reversed(range(6)):
#                 if self.board[row][qubit[0]] == -1:
#                     self.board[row+1][qubit[0]] = measured_value
#                     break
#             # Update value of second qubit after swapping
#             measured_value = self.measure_qubit(qubit[1])
#             for row in reversed(range(6)):
#                 if self.board[row][qubit[1]] == -1:
#                     self.board[row+1][qubit[1]] = measured_value
#                     break
#             print(f"Player {player} updated the board")
#             print(self.board)
#             self.current_player = 1 - self.current_player
#             return
        
#         if action == 'N':
#             self.n_flag +=1 # Incrementing flag value
#             self.current_player = 1 - self.current_player
#             return

#         # Desired outcome aligns with the player's identity (0 or 1)
#         desired_outcome = player

#         # If there is rotation flag, change the qubit of the player
#         if self.n_flag:
#             qubit = 5 - np.random.randint(6)
#             self.n_flag -=1

#         if self.secret_x_pending[qubit]== 0:
#             # Measured when no  X gate applied on the qubit. 
#             current_state = self.measure_qubit(qubit) 
#             # If H gate has been applied to that qubit
#         elif self.state_before_hgate[qubit]==0 or self.state_before_hgate[qubit]==1:
#             current_state= self.state_before_hgate[qubit]
#             self.state_before_hgate[qubit] = -1
#         else:
#             # We only want to measure if there is no X gate applied to that qubit. But if there is 1, we reverse the qubit being measured because the other player when playing their turn won't havre an idea of the X gate. 
#             current_state = self.measure_qubit(qubit)
#             # print(self.secret_x_pending[qubit])
#             current_state = 1- current_state
        
#         if current_state != desired_outcome:
#             self.qc.x(qubit)  # Apply an X gate to achieve desired outcome

#         if self.h_flag[qubit] ==0:
#             measured_value = self.measure_qubit(qubit)  # Measure after adjustments
#         else:
#             # initialising value after Hadamard gate
#             measured_value = self.measure_qubit(qubit)
#             self.h_flag[qubit] -=1
#             # Initialising value once the qubit that had a Hadamard gate was measured to avoid any future discrepencies
#             if measured_value ==1:
#                 self.qc.initialize([0, 1], qubit)
#             else:
#                 self.qc.initialize([1, 0], qubit)

#         # Update the board in the lowest available row for the qubit
#         for row in reversed(range(6)):
#             if self.board[row][qubit] == -1:
#                 self.board[row][qubit] = measured_value
#                 break
#         print(f"Player {player} updated the board:")

#         print(self.board)
#         if self.board[0][qubit] != -1:
#             self.filled_column[qubit] = 1
            
#         self.current_player = 1 - self.current_player
#         return self.board
    
#     def win_condition(self):
#         # Check horizontal lines for a win condition
#         for row in range(6):  # there are 6 rows in a 6x6 board
#             for col in range(3):  # up to the 3rd column to have space for four in a row
#                 if (self.board[row][col] == self.board[row][col + 1] ==
#                     self.board[row][col + 2] == self.board[row][col + 3] != -1):
#                     return True

#         # Check vertical lines for a win condition
#         for col in range(6):  # there are 6 columns in a 6x6 board
#             for row in range(3):  # up to the 3rd row to have space for four in a row
#                 if (self.board[row][col] == self.board[row + 1][col] ==
#                     self.board[row + 2][col] == self.board[row + 3][col] != -1):
#                     return True

#         # Check diagonal lines (down-right) for a win condition
#         for row in range(3):  # up to the 3rd row to have space for diagonal four in a row
#             for col in range(3):  # up to the 3rd column to have space for diagonal four in a row
#                 if (self.board[row][col] == self.board[row + 1][col + 1] ==
#                     self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != -1):
#                     return True

#         # Check diagonal lines (up-right) for a win condition
#         for row in range(3, 6):  # start from the 4th row to the last to have space for diagonal four in a row
#             for col in range(3):  # up to the 3rd column to have space for diagonal four in a row
#                 if (self.board[row][col] == self.board[row - 1][col + 1] ==
#                     self.board[row - 2][col + 2] == self.board[row - 3][col + 3] != -1):
#                     return True

#         return False