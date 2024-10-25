import streamlit as st
import sys
sys.path.append('C:\\Users\\avina\\PycharmProjects\\QC-API-v1')
from qkd.generate_t22_key import phi_plus, phi_minus, psi_plus, psi_minus, Pairing, circuit00, circuit01, circuit10, circuit11
from qkd.generate_t22_key import generate_random_pairings, generate_random_groupings, quantum_compute, generate_code
from qkd.generate_bb84_key import bb84_qkd_protocol_v2
from qkd.generate_e91_key import e91_qkd_protocol_v2
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer
from qiskit.visualization import circuit_drawer
from PIL import Image
import io
import time

# [Keep all existing functions: page_bell_states, page_entangled_states, page_final_circuit]
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

page_bell_states()
page_entangled_states()
page_final_circuit()