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
        self.secret_x_pending = [0] * 6  # Track pending secret X gates
        self.state_before_hgate = [-1] * 6 # Storing measurement value before applying H gate
        self.h_flag = [0] * 6 # Tracking H gate for each qubit
        self.n_flag = 0 # Tracking Rotation gate for each qubit
        self.filled_column = [0]*6
        self.cnot_flag = [0] * 6  # Track CNOT gate applications for target qubits

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
            self.secret_x_pending[qubits] += 1
            self.current_player = 1 - self.current_player
            return  
        
        if action == 'H':
            self.h_flag[qubits] += 1
            self.state_before_hgate[qubits] = self.measure_qubit(qubits)
            self.qc.h(qubits)
            print(f"Player {player} played Hadamard gate on qubit {qubits}:")
            self.current_player = 1 - self.current_player
            return 
        
        if action == 'S':
            self.qc.swap(self.qr[qubits[0]], self.qr[qubits[1]])
            measured_value = self.measure_qubit(qubits[0])
            for row in reversed(range(6)):
                if self.board[row][qubits[0]] == -1:
                    self.board[row + 1][qubits[0]] = measured_value
                    break
            measured_value = self.measure_qubit(qubits[1])
            for row in reversed(range(6)):
                if self.board[row][qubits[1]] == -1:
                    self.board[row + 1][qubits[1]] = measured_value
                    break
            print(f"Player {player} updated the board")
            print(self.board)
            self.current_player = 1 - self.current_player
            return
        
        if action == 'N':
            self.n_flag += 1
            self.current_player = 1 - self.current_player
            return

        if action == 'C':
            control_qubit, target_qubit = qubits
            control_value = self.measure_qubit(control_qubit)
            if control_value == 1:
                self.cnot_flag[target_qubit] = 1  # Set the CNOT flag for the target qubit
            print(f"Player {player} applied CNOT gate with control qubit {control_qubit} and target qubit {target_qubit}")
            print(self.board)
            self.current_player = 1 - self.current_player
            return

        desired_outcome = player

        if self.n_flag:
            qubits = 5 - np.random.randint(6)
            self.n_flag -= 1

        if self.secret_x_pending[qubits] == 0:
            current_state = self.measure_qubit(qubits)
        elif self.state_before_hgate[qubits] == 0 or self.state_before_hgate[qubits] == 1:
            current_state = self.state_before_hgate[qubits]
            self.state_before_hgate[qubits] = -1
        else:
            current_state = self.measure_qubit(qubits)
            current_state = 1 - current_state
        
        if current_state != desired_outcome:
            self.qc.x(qubits)

        if self.h_flag[qubits] == 0:
            measured_value = self.measure_qubit(qubits)
        else:
            measured_value = self.measure_qubit(qubits)
            self.h_flag[qubits] -= 1
            if measured_value == 1:
                self.qc.initialize([0, 1], qubits)
            else:
                self.qc.initialize([1, 0], qubits)

        if self.cnot_flag[qubits] == 1:
            measured_value = 1 - measured_value  # Flip the measured value
            self.cnot_flag[qubits] = 0  # Reset the flag

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
        for row in range(6):
            for col in range(3):
                if (self.board[row][col] == self.board[row][col + 1] ==
                    self.board[row][col + 2] == self.board[row][col + 3] != -1):
                    return True, self.board[row][col]

        for col in range(6):
            for row in range(3):
                if (self.board[row][col] == self.board[row + 1][col] ==
                    self.board[row + 2][col] == self.board[row + 3][col] != -1):
                    return True, self.board[row][col]

        for row in range(3):
            for col in range(3):
                if (self.board[row][col] == self.board[row + 1][col + 1] ==
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != -1):
                    return True, self.board[row][col]

        for row in range(3, 6):
            for col in range(3):
                if (self.board[row][col] == self.board[row - 1][col + 1] ==
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3] != -1):
                    return True, self.board[row][col]

        return False, False
