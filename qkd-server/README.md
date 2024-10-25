# Quantum Key Distribution (QKD) Server

## Overview

This server hosts multiple APIs that demonstrate the concept of Quantum Key Distribution (QKD) using entangled Bell states. QKD is a secure communication method that leverages quantum mechanics to establish a shared secret key between two parties, ensuring secure data transmission.

## APIs

The server includes the following APIs:

- **QKD API**: Provides endpoints for generating quantum keys.
- **DICOM API**: Handles medical imaging data.
- **Chatbot API**: Powers a chatbot application.


## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/CubeStar1/QuantumChat.git
   cd qkd-server
   ```

## Starting the APIs

You can start the APIs using the provided `start.py` script or manually via PowerShell.

### Using `start.py`

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

### Manually via PowerShell

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

## API Endpoints

- **QKD API**: Accessible at `http://localhost:8000`
- **DICOM API**: Accessible at `http://localhost:8001`
- **Chatbot API**: Accessible at `http://localhost:8002`

## Notes

- Ensure that the ports are available and not blocked by any firewall settings.
- The scripts are designed to run on Windows using PowerShell. If you encounter any issues, ensure that your PowerShell execution policy allows running scripts. You can set it temporarily by running:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
