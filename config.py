import os
import sqlite3
import shutil
import time
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from flask import Flask, redirect, url_for, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Apply Cross-Origin Resource Sharing to limit accepting requests from the localhost at port 3000.
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Create thread-local storage for the database connection
local_storage = threading.local()
SCAN_DIRECTORY = "scannedImages"

# Update login configurations
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
                    
loggers = ['socketio', 'engineio', 'werkzeug']

for logger in loggers:
    logging.getLogger(logger).setLevel(logging.CRITICAL)
