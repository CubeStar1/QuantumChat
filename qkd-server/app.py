import streamlit as st
from app_functions import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer
from qiskit.visualization import circuit_drawer
from PIL import Image
import io

def page_bell_states():
    st.title("Bell States")
    with st.container(border=True):
        q = QuantumRegister(2)
        b = ClassicalRegister(2)
        qc1 = QuantumCircuit(q, b)
        qc2 = QuantumCircuit(q, b)
        qc3 = QuantumCircuit(q, b)
        qc4 = QuantumCircuit(q, b)

        phi_plus(q[0], q[1], qc1)
        phi_minus(q[0], q[1], qc2)
        psi_plus(q[0], q[1], qc3)
        psi_minus(q[0], q[1], qc4)

        for qc, state in zip([qc1, qc2, qc3, qc4], ['Phi Plus', 'Phi Minus', 'Psi Plus', 'Psi Minus']):
            with st.container(border=True):
                col1, col2 = st.columns([1,2])
                with col1:
                    st.header(state)
                with col2:
                    image = circuit_drawer(qc, output='mpl')
                    byte_array = io.BytesIO()
                    image.savefig(byte_array, format='PNG')
                    image = Image.open(byte_array)
                    st.image(image)

def page_entangled_states():
    st.title("Entangled Bell States")
    with st.container(border=True):
        q = QuantumRegister(4)
        b = ClassicalRegister(4)
        pairs = Pairing([0, 1], [2, 3])

        qc1, _ = circuit00(pairs)
        qc2, _ = circuit01(pairs)
        qc3, _ = circuit10(pairs)
        qc4, _ = circuit11(pairs)

        for qc, state in zip([qc1, qc2, qc3, qc4], ['Group 00', 'Group 01', 'Group 10', 'Group 11']):
            with st.container(border=True):
                col1, col2 = st.columns([1,2])
                with col1:
                    st.header(state)
                with col2:
                    image = circuit_drawer(qc, output='mpl')
                    byte_array = io.BytesIO()
                    image.savefig(byte_array, format='PNG')
                    image = Image.open(byte_array)
                    st.image(image)

def page_final_circuit():
    st.title("Final Circuit which generates a 2-bit key")
    with st.container(border=True):
        q = QuantumRegister(4)
        b = ClassicalRegister(4)
        qc = QuantumCircuit(q, b)

        # Alice applies a particular pairing and grouping to generate a Bell state
        # For example, let's generate the Bell state for group 00 (phi_plus and phi_minus)

        # Apply a Hadamard gate to the first qubit of the first pair
        qc.h(q[0])

        # Apply a CNOT gate with the first qubit of the first pair as control and the second qubit as target
        qc.cx(q[0], q[1])

        # Apply an X gate to the first qubit of the second pair
        qc.x(q[2])

        # Apply a Hadamard gate to the first qubit of the second pair
        qc.h(q[2])

        # Apply a CNOT gate with the first qubit of the second pair as control and the second qubit as target
        qc.cx(q[2], q[3])

        # Bob applies the reverse circuit
        # For the reverse circuit of group 00 (phi_plus_reverse and phi_minus_reverse)

        # Apply a CNOT gate with the first qubit of the first pair as control and the second qubit as target
        qc.cx(q[0], q[1])

        # Apply a Hadamard gate to the first qubit of the first pair
        qc.h(q[0])

        # Apply a CNOT gate with the first qubit of the second pair as control and the second qubit as target
        qc.cx(q[2], q[3])

        # Apply a Hadamard gate to the first qubit of the second pair
        qc.h(q[2])

        # Apply an X gate to the first qubit of the second pair
        qc.x(q[2])

        qc.measure_all()

        # Convert the quantum circuit to an image
        image = circuit_drawer(qc, output='mpl')

        # Convert image to byte array
        byte_array = io.BytesIO()
        image.savefig(byte_array, format='PNG')

        # Convert byte array to PIL image
        image = Image.open(byte_array)

        # Display the image on Streamlit
        col1, col2 = st.columns([1,2])
        with col1:
            st.header('Final Circuit')
        with col2:
            st.image(image, caption='Final Circuit')

import time

def page_shared_key():
    st.title("Generate Shared Key")
    with st.container(border=True):
        desired_key_length = st.number_input('Enter desired key length:', min_value=1, max_value=1000, value=10)

        if st.button('Generate Shared Key', key='generate_shared_key'):

            start_time = time.time()

            alice_code, bob_code = "", ""
            while len(alice_code) <= desired_key_length:
                alice_pairings = generate_random_pairings(10)
                alice_groupings = generate_random_groupings(10)
                bob_pairings = generate_random_pairings(10)
                bob_groupings = generate_random_groupings(10)

                alice_json = {"pairings": alice_pairings, "groupings": alice_groupings, "correct_measurements": []}
                bob_json = {"pairings": bob_pairings, "groupings": bob_groupings, "correct_measurements": []}
                alice_json, bob_json = quantum_compute(alice_json, bob_json)
                alice_json, bob_json = quantum_compute(alice_json, bob_json)
                alice_json["code"] = generate_code(alice_json["correct_measurements"])
                bob_json["code"] = generate_code(bob_json["correct_measurements"])
                alice_code += alice_json["code"]
                bob_code += bob_json["code"]

            alice_code = alice_code[:desired_key_length]
            bob_code = bob_code[:desired_key_length]

            end_time = time.time()
            time_taken = end_time - start_time

            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Alice Code')
                st.write(alice_code)
            with col2:
                st.subheader('Bob Code')
                st.write(bob_code)

            st.write(f"Time taken to generate the key: {int(time_taken)} seconds")
PAGES = {
    "Bell States": page_bell_states,
    "Entangled Bell States": page_entangled_states,
    "Final Circuit": page_final_circuit,
    "Generate Shared Key": page_shared_key
}

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", list(PAGES.keys()))

    PAGES[choice]()

if __name__ == "__main__":
    main()