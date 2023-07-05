#!/usr/bin/env python3

import os
import subprocess
import threading
import time

# Global Constants
SCANNED_IMAGES_DIR = 'scannedImages'
REACT_APP_DIR = 'front-end'

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
    flask_process = subprocess.Popen(["python3", "server.py"])

# Run react app in the background
def run_react_app():
    os.chdir(REACT_APP_DIR)
    global react_process
    env = os.environ.copy()
    env["BROWSER"] = "none"  # Set BROWSER environment variable
    react_process = subprocess.Popen(["npm", "start"], env=env)  
    os.chdir("..") 

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
            subprocess.call(["python3", "scan.py"])  

        elif user_input == '2':
            print(f"You can now explore the image database by navigating to this URL: http://localhost:3000")

        elif user_input == '3':
            print("Shutting down the servers and exiting the program. Bye!")
            flask_process.terminate()  # Try to stop the Flask server
            react_process.terminate()  # Try to stop the React app
            time.sleep(6)  
            if flask_process.poll() is None:  # If the Flask server is still running
                flask_process.kill()  
            if react_process.poll() is None:  # If the React app is still running
                react_process.kill()  
            os._exit(0)  # Terminate all threads

        else:
            print("Error: Invalid input! Please enter a number between 1 and 3.")

if __name__ == '__main__':
    try:
        create_directory()
        run_react_app()  # Run the React app
        t = threading.Thread(target=run_flask_app) # Run the Flask server
        t.start()
        print("Starting the servers... This may take a few moments.")
        time.sleep(6)  # Give the server a bit of time to start
        main_menu()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
