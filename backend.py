from flask import Flask, render_template, redirect, url_for, request ,send_from_directory , jsonify
import sqlite3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import shutil
import time
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

import logging
logging.getLogger('socketio').setLevel(logging.CRITICAL)
logging.getLogger('engineio').setLevel(logging.CRITICAL)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Create thread-local storage for the database connection
local_storage = threading.local()

def get_db():
    if not hasattr(local_storage, 'db'):
        local_storage.db = sqlite3.connect('image_database.db')
        local_storage.db.execute('PRAGMA foreign_keys = ON')  # Enable foreign key support
    return local_storage.db

# Create the table if it doesn't exist
def create_table():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT,
            metadata TEXT
        )
    ''')
    db.commit()

# Define the event handler for new folder creation and deletion
class FolderEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            folder_path = event.src_path
            folder_name = os.path.basename(folder_path)

            # Wait until metadata.txt file is available
            while not os.path.exists(os.path.join(folder_path, 'metadata.txt')):
                time.sleep(0.1)

            # Read the metadata from the text file
            with open(os.path.join(folder_path, 'metadata.txt'), 'r') as file:
                metadata = file.read()

            # Insert the folder name and metadata into the database
            db = get_db()
            db.execute('INSERT INTO images (folder_name, metadata) VALUES (?, ?)', (folder_name, metadata))
            db.commit()
            socketio.emit('folder_updated')

    def on_deleted(self, event):
        if event.is_directory:
            folder_path = event.src_path
            folder_name = os.path.basename(folder_path)

            # Delete the corresponding record from the database
            db = get_db()
            db.execute('DELETE FROM images WHERE folder_name = ?', (folder_name,))
            db.commit()
            socketio.emit('folder_updated')
# Create an observer and assign the event handler
observer = Observer()
event_handler = FolderEventHandler()

# Set the directory to monitor
scanned_images_dir = 'scannedImages'

# Schedule the observer to watch for new folder creations and deletions
observer.schedule(event_handler, scanned_images_dir, recursive=False)
observer.start()

@app.route('/image/<folder_name>/<filename>')
def serve_image(folder_name, filename):
    safe_folder_name = secure_filename(folder_name)
    safe_filename = secure_filename(filename)
    return send_from_directory(os.path.join(scanned_images_dir, safe_folder_name), safe_filename)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.get_json().get('search', '')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM images WHERE metadata LIKE ?', ('%' + search_query + '%',))
        rows = cursor.fetchall()
        cursor.close()

        # Convert rows to list of dictionaries
        rows = [{'id': row[0], 'folder_name': row[1], 'metadata': row[2]} for row in rows]

        return jsonify(rows)

    else:
        # Fetch all rows from the 'images' table
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM images')
        rows = cursor.fetchall()
        cursor.close()

    # Render the HTML template and pass the rows to it
    # return render_template('index.html', rows=rows)
    rows = [{'id': row[0], 'folder_name': row[1], 'metadata': row[2]} for row in rows]
    return jsonify(rows)

# Route for deleting a folder
@app.route('/delete/<int:folder_id>', methods=['POST'])
def delete_folder(folder_id):
    # Retrieve the folder name from the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT folder_name FROM images WHERE id = ?', (folder_id,))
    folder_name = cursor.fetchone()[0]

    # Delete the folder from the 'scannedImages' directory
    folder_path = os.path.join(scanned_images_dir, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

    # Delete the corresponding record from the database
    cursor.execute('DELETE FROM images WHERE id = ?', (folder_id,))
    db.commit()
    cursor.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()

    try:
        # app.run(debug=False, use_reloader=False)
        socketio.run(app, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    # Close the database connection
    db = get_db()
    db.close()