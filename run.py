#!/usr/bin/env python3

import os
import subprocess
import threading
import time

# Global Constants
SCANNED_IMAGES_DIR = 'scannedImages'
REACT_APP_DIR = 'frontend'

# Global variables for tracking processes
flask_process = None
react_process = None

# Function to check and create directory
def create_directory():
    if not os.path.exists(SCANNED_IMAGES_DIR):
        os.makedirs(SCANNED_IMAGES_DIR)
        print(f"Success: The directory {SCANNED_IMAGES_DIR} has been created!")
    else:
        print(f"Info: The directory {SCANNED_IMAGES_DIR} already exists.")

# Run flask app in the background
def run_flask_app():
    global flask_process
    flask_process = subprocess.Popen(["python3", "backend.py"])

# Run react app in the background
def run_react_app():
    os.chdir(REACT_APP_DIR)
    subprocess.call(["npm", "run build"])  # Build the react app
    global react_process
    env = os.environ.copy()  # Get a copy of the current environment variables
    env["BROWSER"] = "none"  # Set BROWSER environment variable
    react_process = subprocess.Popen(["npm", "start"], env=env)  # Start the react app with the new environment
    os.chdir("..")  # Change back to the original directory

def main_menu():
    while True:
        print("\n----- Main Menu -----")
        print("Please choose one of the options:")
        print("1: Run Scanner")
        print("2: Explore Image Database")
        print("3: Exit the Program")

        user_input = input("Please enter the option number (1-3): ")

        if user_input == '1':
            print("Running the scanner... This may take a few moments.")
            subprocess.call(["python3", "scan.py"])  # Assuming scan.py is in the same directory

        elif user_input == '2':
            print(f"You can now explore the image database by navigating to this URL: http://localhost:3000")

        elif user_input == '3':
            print("Shutting down the servers and exiting the program. Bye!")
            flask_process.terminate()  # Try to gracefully stop the Flask server
            react_process.terminate()  # Try to gracefully stop the React app
            time.sleep(6)  # Give the processes some time to stop
            if flask_process.poll() is None:  # If the Flask server is still running
                flask_process.kill()  # Forcefully stop the Flask server
            if react_process.poll() is None:  # If the React app is still running
                react_process.kill()  # Forcefully stop the React app
            os._exit(0)  # Use os._exit to terminate all threads

        else:
            print("Error: Invalid input! Please enter a number between 1 and 3.")

def main():
    try:
        create_directory()
        run_react_app()  # Run the React app
        t = threading.Thread(target=run_flask_app)
        t.start()
        print("Starting the servers... This may take a few moments.")
        time.sleep(6)  # Give the server a bit of time to start
        main_menu()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
