# Quantum Key Distribution Simulator

This project demonstrates the concept of Quantum Key Distribution using Qiskit and Streamlit. The Streamlit app allows users to generate Bell states, entangled Bell states, and a final circuit. It also provides an endpoint to generate a shared key using quantum computations.



## About Quantum Key Distribution using Entangled Bell States

- Quantum Key Distribution (QKD) is a method of secure communication that uses quantum mechanics to secure a communication channel. One of the most well-known QKD protocols is the BB84 protocol, which uses qubits to generate a shared secret key between two parties.
- This project demonstrates the concept of QKD using entangled Bell states. Bell states are a set of four maximally entangled quantum states that form the basis for many quantum communication protocols.
- In this method, two parties, commonly referred to as Alice and Bob, generate a shared secret key that can be used for encrypting and decrypting messages. The security of the key is guaranteed by the laws of quantum mechanics, specifically the principle of quantum entanglement and the no-cloning theorem.
- In the context of this project, the entangled Bell states are used to generate a shared key between Alice and Bob. The `generate_key.py` script defines a FastAPI application with a single `GET endpoint /key/{desired_key_length}`. This endpoint generates a shared key of a specified length using quantum computations. The generated key is then used in another chat application to generate symmetric keys for encryption.

## File Descriptions

- `app.py`: This is the main Python script where the Streamlit app is defined. It contains several pages such as "Bell States", "Entangled Bell States", "Final Circuit", and "Generate Shared Key". Each page is a function that defines the layout and functionality of that page.

- `app_functions.py`: This file contains the functions `quantum_compute` and `generate_code` used in the `app.py` and `generate_key.py` scripts.

- `generate_key.py`: This script defines a FastAPI application with a single GET endpoint `/key/{desired_key_length}`. The endpoint generates a shared key of a specified length using quantum computations. This endpoint is used in another chat application to generate symmetric keys for encryption.

- `requirements.txt`: This file lists the Python packages required for the project. It includes packages like `streamlit`, `qiskit`, `pillow`, `pytest`, and `fastapi`.


## Running the Streamlit App

To run the Streamlit app, follow these steps:

1. Ensure you have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).

2. Install the required Python packages. In the root directory of the project, run the following command:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

4. Open your browser and go to `http://localhost:8501` to view the app.

