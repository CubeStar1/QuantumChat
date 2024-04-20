from qiskit import Aer
from qiskit import execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import circuit_drawer
from PIL import Image
import io
import random
import json

qbits = 4

class Pairing:
    def __init__(self, pair1, pair2):
        self.bit0 = pair1[0]
        self.bit1 = pair1[1]
        self.bit2 = pair2[0]
        self.bit3 = pair2[1]

def phi_plus(bit0, bit1, qc):
    qc.h(bit0)
    qc.cx(bit0, bit1)

def phi_minus(bit0, bit1, qc):
    qc.x(bit0)
    qc.h(bit0)
    qc.cx(bit0, bit1)

def psi_plus(bit0, bit1, qc):
    qc.h(bit0)
    qc.x(bit1)
    qc.cx(bit0, bit1)

def psi_minus(bit0, bit1, qc):
    qc.h(bit0)
    qc.x(bit1)
    qc.z(bit0)
    qc.z(bit1)
    qc.cx(bit0, bit1)

def circuit00(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    phi_plus(q[pairs.bit0], q[pairs.bit1], qc)
    phi_minus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 00")
    return qc, q

def circuit01(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    phi_minus(q[pairs.bit0], q[pairs.bit1], qc)
    phi_plus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 01")
    return qc, q

def circuit10(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    psi_plus(q[pairs.bit0], q[pairs.bit1], qc)
    psi_minus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 10")
    return qc, q

def circuit11(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    psi_minus(q[pairs.bit0], q[pairs.bit1], qc)
    psi_plus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 11")
    return qc, q

################################
# Generate Reverse Bell States #
################################
def phi_plus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.h(bit0)

def phi_minus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.h(bit0)
    qc.x(bit0)

def psi_plus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.x(bit1)
    qc.h(bit0)

def psi_minus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.z(bit1)
    qc.z(bit0)
    qc.x(bit1)
    qc.h(bit0)

#############################################
# Generate Reverse Pair-Entangling Circuits #
#############################################
def reverse_circuit00(pairs, q, qc):
    phi_plus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    phi_minus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    print("Bob chose group 00")

def reverse_circuit01(pairs, q, qc):
    phi_minus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    phi_plus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    print("Bob chose group 01")
    # print(qc)

def reverse_circuit10(pairs, q, qc):
    psi_plus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    psi_minus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    print("Bob chose group 10")
    # print(qc)

def reverse_circuit11(pairs, q, qc):
    psi_minus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    psi_plus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    print("Bob chose group 11")
    # print(qc)

def generate_random_pairings(length):
    all_pairings = [[[0,1], [2,3]], [[0,2], [1,3]], [[0,3], [1,2]]]
    return [random.choice(all_pairings) for _ in range(length)]

def generate_random_groupings(length):
    return [random.randint(0,3) for _ in range(length)]


def get_correct_measurements(alice_json, bob_json):
    indices = alice_json["correct_measurements"]
    alice_initial_pairings = alice_json["pairings"]
    alice_initial_groupings = alice_json["groupings"]

    bob_initial_pairings = bob_json["pairings"]
    bob_initial_groupings = bob_json["groupings"]

    alice_correct = {"pairings": [], "groupings": []}
    bob_correct = {"pairings": [], "groupings": []}

    # use quantum measurements to get correct values
    for i in indices:
        alice_correct["pairings"].append(alice_initial_pairings[i])
        alice_correct["groupings"].append(alice_initial_groupings[i])
        bob_correct["pairings"].append(bob_initial_pairings[i])
        bob_correct["groupings"].append(bob_initial_groupings[i])

    return alice_correct, bob_correct
def verify_circuit(qc):
    qc.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=256)
    #qc.measure_all()
    #job = execute(qc, backend=QI_BACKEND, shots=256)
    result = job.result()
    histogram = result.get_counts(qc)
    print(histogram)

    # If Bob guessed Alice's qubit-pairs and Bell states correctly,
    # the final state of all qubits should be 0s
    state_list = list(histogram.keys())
    print(state_list)
    if (len(state_list) == 1 and state_list[0] == "0000 0000"):
        return 1
    return 0

entangling_circuit_map = {0: circuit00, 1: circuit01, 2: circuit10, 3: circuit11}
reversal_circuit_map = {0: reverse_circuit00, 1: reverse_circuit01, 2: reverse_circuit10, 3: reverse_circuit11}
def quantum_compute(alice_data, bob_data):
    alice_qpairs = alice_data["pairings"]
    alice_groupcodes = alice_data["groupings"]

    bob_qpairs = bob_data["pairings"]
    bob_groupcodes = bob_data["groupings"]

    # Keeps track of the indices in Bob's list that were correct guesses
    correct_guesses = []

    for i in range(len(alice_qpairs)): # iterate over  qubit-pairs

        # Obtain both users' group codes
        alice_gc = alice_groupcodes[i]
        bob_gc = bob_groupcodes[i]

        qpairs = Pairing(alice_qpairs[i][0], alice_qpairs[i][1])

        # Build Alice's circuits based on her inputs
        qc, q = entangling_circuit_map[alice_gc](qpairs)

        qpairs = Pairing(bob_qpairs[i][0], bob_qpairs[i][1])

        # Run Bob's test circuits on top of Alice's input
        reversal_circuit_map[bob_gc](qpairs, q, qc)

        # Add the index to the list of correct guesses to return to the users
        if (verify_circuit(qc)):
            correct_guesses.append(i)
            print("Bob's guess was correct")

    alice_data["correct_measurements"] = correct_guesses
    bob_data["correct_measurements"] = correct_guesses

    return alice_data, bob_data

def generate_code(groupings):
    code = ""
    for i in groupings:
        if i == 0:
            code += "00"
        if i == 1:
            code += "01"
        if i == 2:
            code += "10"
        if i == 3:
            code += "11"
    return code