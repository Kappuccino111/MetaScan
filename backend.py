"""A File for configuring the backend on flask and sqllite """
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
    """Get a SQLite database connection."""
    if not hasattr(local_storage, 'db'):
        local_storage.db = sqlite3.connect('image_database.db')
        local_storage.db.execute('PRAGMA foreign_keys = ON')  # Enable foreign key support
    return local_storage.db


def create_table():
    """Create a table if it doesn't exist."""
    database = get_db()
    database.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT,
            metadata TEXT
        )
    ''')
    database.commit()


class FolderEventHandler(FileSystemEventHandler):
    """Event handler for new folder creation and deletion."""

    def on_created(self, event):
        """Called when a directory is created."""
        if event.is_directory:
            folder_path = event.src_path
            folder_name = os.path.basename(folder_path)

            # Wait until metadata.txt file is available
            while not os.path.exists(os.path.join(folder_path, 'metadata.txt')):
                time.sleep(0.1)

            # Read the metadata from the text file
            with open(os.path.join(folder_path, 'metadata.txt'), 'r', encoding='utf-8') as file:
                metadata = file.read()

            # Insert the folder name and metadata into the database
            database = get_db()
            database.execute('INSERT INTO images (folder_name, metadata) VALUES (?, ?)',
             (folder_name, metadata))
            database.commit()
            socketio.emit('folder_updated')

    def on_deleted(self, event):
        """Called when a directory is deleted."""
        if event.is_directory:
            folder_path = event.src_path
            folder_name = os.path.basename(folder_path)

            # Delete the corresponding record from the database
            database = get_db()
            database.execute('DELETE FROM images WHERE folder_name = ?', (folder_name,))
            database.commit()
            socketio.emit('folder_updated')


@app.route('/image/<folder_name>/<filename>')
def serve_image(folder_name, filename):
    """Serve an image file."""
    safe_folder_name = secure_filename(folder_name)
    safe_filename = secure_filename(filename)
    return send_from_directory(os.path.join(SCAN_DIRECTORY, safe_folder_name), safe_filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage route."""
    if request.method == 'POST':
        search_query = request.get_json().get('search', '')

        database = get_db()
        cursor = database.cursor()
        cursor.execute('SELECT * FROM images WHERE metadata LIKE ?', ('%' + search_query + '%',))
        rows = cursor.fetchall()
        cursor.close()

        # Convert rows to list of dictionaries
        rows = [{'id': row[0], 'folder_name': row[1], 'metadata': row[2]} for row in rows]

        return jsonify(rows)

    else:
        # Fetch all rows from the 'images' table
        database = get_db()
        cursor = database.cursor()
        cursor.execute('SELECT * FROM images')
        rows = cursor.fetchall()
        cursor.close()

    # Render the HTML template and pass the rows to it
    # return render_template('index.html', rows=rows)
    rows = [{'id': row[0], 'folder_name': row[1], 'metadata': row[2]} for row in rows]
    return jsonify(rows)


@app.route('/delete/<int:folder_id>', methods=['POST'])
def delete_folder(folder_id):
    """Delete a folder."""
    # Retrieve the folder name from the database
    database = get_db()
    cursor = database.cursor()
    cursor.execute('SELECT folder_name FROM images WHERE id = ?', (folder_id,))
    folder_name = cursor.fetchone()[0]

    # Delete the folder from the 'scannedImages' directory
    folder_path = os.path.join(SCAN_DIRECTORY, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

    # Delete the corresponding record from the database
    cursor.execute('DELETE FROM images WHERE id = ?', (folder_id,))
    database.commit()
    cursor.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    create_table()

    SCAN_DIRECTORY = 'scannedImages'
    observer = Observer()
    event_handler = FolderEventHandler()
    observer.schedule(event_handler, SCAN_DIRECTORY, recursive=False)
    observer.start()

    try:
        # app.run(debug=False, use_reloader=False)
        socketio.run(app, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    # Close the database connection
    db = get_db()
    db.close()
