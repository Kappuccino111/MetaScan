import os
import time
from watchdog.events import FileSystemEventHandler

from config import socketio
from database import get_db

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
