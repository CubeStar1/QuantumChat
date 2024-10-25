import subprocess
import os

# Define the PowerShell commands
commands = """
# Activate the virtual environment and start the first API
Start-Process powershell -ArgumentList '-NoExit', '\\.venv\\Scripts\\activate; uvicorn qkd.app:app --host 0.0.0.0 --port 8000'

# Activate the virtual environment and start the second API
Start-Process powershell -ArgumentList '-NoExit', '\\.venv\\Scripts\\activate; uvicorn DICOM.app:app --host 0.0.0.0 --port 8001'

# Activate the virtual environment and start the third API
Start-Process powershell -ArgumentList '-NoExit', '.\\venv\\Scripts\\activate; uvicorn chatbot.app:app --host 0.0.0.0 --port 8002'
"""

# Write the commands to a new PowerShell script file
with open('start_apis.ps1', 'w') as f:
    f.write(commands)

# Execute the PowerShell script
subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", os.path.join(os.getcwd(), 'start_apis.ps1')])