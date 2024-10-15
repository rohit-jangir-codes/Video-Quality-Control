import os
import subprocess

# Set the port number to be hardcoded
PORT = 5117

def start_application():
    # Navigate to the directory containing manage.py
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run the Django server on the hardcoded port
    subprocess.run(['python', 'manage.py', 'runserver', f'0.0.0.0:{PORT}'])

if __name__ == "__main__":
    print(f"Starting the Django application on port {PORT}...")
    start_application()
