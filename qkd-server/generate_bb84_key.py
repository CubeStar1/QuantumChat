from fastapi import FastAPI, HTTPException
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
import time

app = FastAPI()


def bb84_qkd_protocol(n_bits):
    qc = QuantumCircuit(n_bits, n_bits)

    # Alice generates random bit string
    alice_bits = np.random.randint(2, size=n_bits)

    # Alice selects random basis for each bit (0 for rectilinear, 1 for diagonal)
    alice_basis = np.random.randint(2, size=n_bits)

    # Bob randomly chooses basis for each received bit
    bob_basis = np.random.randint(2, size=n_bits)

    # Encode qubits based on Alice's random bit string and basis
    for i in range(n_bits):
        if alice_basis[i] == 0:  # Rectilinear basis
            if alice_bits[i] == 1:
                qc.h(i)  # Apply Hadamard gate if bit is 1
        else:  # Diagonal basis
            if alice_bits[i] == 1:
                qc.h(i)  # Apply Hadamard gate if bit is 1
                qc.s(i)  # Apply S gate for diagonal basis

    qc.barrier()

    # Bob measures received qubits based on his chosen basis
    for i in range(n_bits):
        if bob_basis[i] == 0:  # Rectilinear basis
            qc.measure(i, i)
        else:  # Diagonal basis
            qc.sdg(i)
            qc.h(i)
            qc.measure(i, i)

    # Simulate the quantum circuit
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    # Alice and Bob discard bits where bases didn't match
    shared_key = ""
    for key in counts:
        index = int(key, 2) % n_bits
        if alice_basis[index] == bob_basis[index]:
            shared_key += key

    return shared_key


@app.get("/bb84_key/{n_bits}")
async def generate_shared_key(n_bits: int):
    if n_bits <= 0:
        raise HTTPException(status_code=400, detail="Number of bits must be positive")

    st = time.time()

    shared_key = bb84_qkd_protocol(n_bits)

    et = time.time()

    time_taken = et - st

    return {"alice_key": shared_key, "bob_key": shared_key, "time_taken": str(time_taken) }



# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8001)
