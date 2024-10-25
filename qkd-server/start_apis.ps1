
# Activate the virtual environment and start the first API
Start-Process powershell -ArgumentList '-NoExit', '\.venv\Scripts\activate; uvicorn qkd.app:app --host 0.0.0.0 --port 8000'

# Activate the virtual environment and start the second API
Start-Process powershell -ArgumentList '-NoExit', '\.venv\Scripts\activate; uvicorn DICOM.app:app --host 0.0.0.0 --port 8001'

# Activate the virtual environment and start the third API
Start-Process powershell -ArgumentList '-NoExit', '.\venv\Scripts\activate; uvicorn chatbot.app:app --host 0.0.0.0 --port 8002'
