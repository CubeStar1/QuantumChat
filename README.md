# Quantum Chat

Quantum Chat is a secure messaging system that uses Quantum Key Distribution (QKD) for cryptographic key generation and RSA for key exchange. It comprises a NodeJS server, a Svelte client, and a QKD Python server for quantum key generation.

## Key Features

- Server-side component in TypeScript with WebSocket communication
- Client-side component in Svelte using IndexedDB for local storage
- Quantum Key Distribution for generating secure symmetric keys
- Hybrid encryption system combining symmetric and asymmetric encryption
- AES-CTR algorithm for message encryption and decryption

## Setup and Installation

### Prerequisites

- Node.js and npm (for TypeScript server and Svelte client)
- Python 3.7+ and pip (for QKD server)
- PowerShell (for Windows users)

### 1. Clone the Repository

```bash
git clone https://github.com/CubeStar1/QuantumChat.git
cd QuantumChat
```

### 2. QKD Server

```bash
cd qkd-server
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix or MacOS
pip install -r requirements.txt
```


You can start the APIs using the provided `start.py` script or manually.

#### Using `start.py`

1. **Activate the Virtual Environment:**
   Ensure your virtual environment is activated:
   ```bash
   .\.venv\Scripts\activate
   ```

2. **Run the Script:**
   Execute the `start.py` script to generate and run the PowerShell script that starts the APIs:
   ```bash
   python start.py
   ```

#### Manually

1. **Activate the Virtual Environment:**
   ```bash
   .\.venv\Scripts\activate
   ```

2. **Start Each API:**
   - **QKD API**: 
     ```powershell
     uvicorn qkd.app:app --host 0.0.0.0 --port 8000
     ```
   - **DICOM API**: 
     ```powershell
     uvicorn DICOM.app:app --host 0.0.0.0 --port 8001
     ```
   - **Chatbot API**: 
     ```powershell
     uvicorn chatbot.app:app --host 0.0.0.0 --port 8002
     ```

API Endpoints:

- **QKD API**: Accessible at `http://localhost:8000`
- **DICOM API**: Accessible at `http://localhost:8001`
- **Chatbot API**: Accessible at `http://localhost:8002`

### 3. NodeJS Backend

```bash
cd chatapp-server
npm install
```

Start the TypeScript server:
```bash
ts-node server-v3.ts
```

### 4. Svelte Frontend

```bash
cd chatapp-frontend
npm install
```

Start the Svelte development server:
```bash
npm run dev -- --open
```

## Running the Application

1. Ensure the QKD server is running on port 8000
2. Start the NodeJS backend (it will run on port 3000)
3. Launch the Svelte frontend (typically on port 5000 or 5173)
4. Access the application through the URL provided by the Svelte frontend

## Detailed System Architecture

### Server-side (NodeJS)
- Manages WebSocket connections and nicknames
- Handles message routing and key distribution
- Maintains two maps: `connections` and `nicknames`
- Listens for incoming messages and performs actions based on message type

### Client-side (Svelte)
- Maintains WebSocket connection to the server
- Uses IndexedDB to store users and messages
- Handles user interactions, message sending, and conversation management
- Implements encryption and decryption of messages using AES

### QKD Server
- Generates shared keys using quantum computations
- Provides API endpoint for key generation
- Uses FastAPI to handle requests for quantum keys

## Encryption Overview

- Hybrid encryption system using QKD-generated symmetric keys and RSA
- Server encrypts symmetric keys with clients' public RSA keys
- Clients decrypt symmetric keys using their private RSA keys
- Messages encrypted/decrypted using AES algorithm
- Server doesn't store encryption keys; they're generated on-demand for each conversation

## Security Notes

- Client-side encryption/decryption ensures message privacy
- Even if the server is compromised, message content remains secure
- The use of QKD provides forward secrecy and resistance to quantum computing attacks

For more detailed information on each component, refer to their respective README files in the `qkd-server` and `chatapp-server` directories.
