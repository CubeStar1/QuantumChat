import qiskit
# useful additional packages
import numpy as np
import random
# regular expressions module
import re

# importing the QISKit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

# import basic plot tools
from qiskit.tools.visualization import circuit_drawer, plot_histogram
def simulate_e91_protocol(numberOfSinglets):
    # Creating registers
    qr = QuantumRegister(2, name="qr")
    cr = ClassicalRegister(4, name="cr")


    singlet = QuantumCircuit(qr, cr, name='singlet')
    singlet.x(qr[0])
    singlet.x(qr[1])
    singlet.h(qr[0])
    singlet.cx(qr[0],qr[1])



    ## Alice's measurement circuits

    # measure the spin projection of Alice's qubit onto the a_1 direction (X basis)
    measureA1 = QuantumCircuit(qr, cr, name='measureA1')
    measureA1.h(qr[0])
    measureA1.measure(qr[0],cr[0])

    # measure the spin projection of Alice's qubit onto the a_2 direction (W basis)
    measureA2 = QuantumCircuit(qr, cr, name='measureA2')
    measureA2.s(qr[0])
    measureA2.h(qr[0])
    measureA2.t(qr[0])
    measureA2.h(qr[0])
    measureA2.measure(qr[0],cr[0])

    # measure the spin projection of Alice's qubit onto the a_3 direction (standard Z basis)
    measureA3 = QuantumCircuit(qr, cr, name='measureA3')
    measureA3.measure(qr[0],cr[0])

    ## Bob's measurement circuits

    # measure the spin projection of Bob's qubit onto the b_1 direction (W basis)
    measureB1 = QuantumCircuit(qr, cr, name='measureB1')
    measureB1.s(qr[1])
    measureB1.h(qr[1])
    measureB1.t(qr[1])
    measureB1.h(qr[1])
    measureB1.measure(qr[1],cr[1])

    # measure the spin projection of Bob's qubit onto the b_2 direction (standard Z basis)
    measureB2 = QuantumCircuit(qr, cr, name='measureB2')
    measureB2.measure(qr[1],cr[1])

    # measure the spin projection of Bob's qubit onto the b_3 direction (V basis)
    measureB3 = QuantumCircuit(qr, cr, name='measureB3')
    measureB3.s(qr[1])
    measureB3.h(qr[1])
    measureB3.tdg(qr[1])
    measureB3.h(qr[1])
    measureB3.measure(qr[1],cr[1])

    ## Lists of measurement circuits
    aliceMeasurements = [measureA1, measureA2, measureA3]
    bobMeasurements = [measureB1, measureB2, measureB3]


    # Define the number of singlets N



    aliceMeasurementChoices = [random.randint(1, 3) for i in range(numberOfSinglets)] # string b of Alice
    bobMeasurementChoices = [random.randint(1, 3) for i in range(numberOfSinglets)] # string b' of Bob

    circuits = []  # the list in which the created circuits will be stored

    for i in range(numberOfSinglets):
        # create the name of the i-th circuit depending on Alice's and Bob's measurement choices
        circuitName = str(i) + ':A' + str(aliceMeasurementChoices[i]) + '_B' + str(bobMeasurementChoices[i])

        # create the joint measurement circuit
        # add Alice's and Bob's measurement circuits to the singlet state curcuit
        # singlet state circuit # measurement circuit of Alice # measurement circuit of Bob
        #circuitName = singlet + aliceMeasurements[aliceMeasurementChoices[i] - 1] + bobMeasurements[
            #bobMeasurementChoices[i] - 1]
        circuitName = singlet.compose(aliceMeasurements[aliceMeasurementChoices[i] - 1]).compose(
            bobMeasurements[bobMeasurementChoices[i] - 1])
        # add the created circuit to the circuits list
        circuits.append(circuitName)


    backend=Aer.get_backend('qasm_simulator')
    result = execute(circuits, backend=backend, shots=1).result()
    #print(result) # uncomment for detailed result

    print(result.get_counts(circuits[0]))


    abPatterns = [
        re.compile('..00$'), # search for the '..00' output (Alice obtained -1 and Bob obtained -1)
        re.compile('..01$'), # search for the '..01' output
        re.compile('..10$'), # search for the '..10' output (Alice obtained -1 and Bob obtained 1)
        re.compile('..11$')  # search for the '..11' output
    ]


    # create a list to store the results

    aliceResults = []  # Alice's results (string a)
    bobResults = []  # Bob's results (string a')

    for i in range(numberOfSinglets):
        res = list(result.get_counts(circuits[i]).keys())[0]
        if abPatterns[0].search(res):
            aliceResults.append(1)
            bobResults.append(1)
        if abPatterns[1].search(res):
            aliceResults.append(0)
            bobResults.append(1)
        if abPatterns[2].search(res):
            aliceResults.append(1)
            bobResults.append(0)
        if abPatterns[3].search(res):
            aliceResults.append(0)
            bobResults.append(0)

    aliceKey = []
    bobKey = []

    for i in range(numberOfSinglets):
        if (aliceMeasurementChoices[i] == 2 and bobMeasurementChoices[i] == 1) or (
                aliceMeasurementChoices[i] == 3 and bobMeasurementChoices[i] == 2):
            if aliceResults[i] == bobResults[i]:  # Only append when Alice's and Bob's results match
                aliceKey.append(aliceResults[i])
                bobKey.append(bobResults[i])

    keyLength = len(aliceKey)  # length of the secret key


    abKeyMismatches = 0 # number of mismatching bits in Alice's and Bob's keys

    for j in range(keyLength):
        if aliceKey[j] != bobKey[j]:
            abKeyMismatches += 1

    print("The number of mismatching bits in Alice's and Bob's keys is", abKeyMismatches)
    print("The length of the secret key is", keyLength)
    print("The secret key is", aliceKey)
    print("The secret key is", bobKey)

    return aliceKey, bobKey

def e91_qkd_protocol(desired_key_length):
    final_alice_key = []
    final_bob_key = []

    while len(final_alice_key) < desired_key_length and len(final_bob_key) < desired_key_length:
        aliceKey, bobKey = simulate_e91_protocol(desired_key_length)
        final_alice_key.extend(aliceKey)
        final_bob_key.extend(bobKey)

    # Truncate the keys to the desired length
    final_alice_key = final_alice_key[:desired_key_length]
    final_bob_key = final_bob_key[:desired_key_length]

    # Convert the keys to strings
    final_alice_key = ''.join(map(str, final_alice_key))
    final_bob_key = ''.join(map(str, final_bob_key))

    return final_alice_key, final_bob_key


