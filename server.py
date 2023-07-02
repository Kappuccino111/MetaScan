import os
import shutil
import config
from watchdog.observers import Observer

from config import app, socketio, SCAN_DIRECTORY, secure_filename
from database import create_table, get_db
from file_system_handler import FolderEventHandler


@app.route('/image/<folder_name>/<filename>')
def serve_image(folder_name, filename):
    """Serve an image file."""
    safe_folder_name = secure_filename(folder_name)
    safe_filename = secure_filename(filename)
    return config.send_from_directory(os.path.join(SCAN_DIRECTORY, safe_folder_name), safe_filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage route."""
    if config.request.method == 'POST':
        search_query = config.request.get_json().get('search', '')

        database = get_db()
        cursor = database.cursor()
        cursor.execute('SELECT * FROM images WHERE metadata LIKE ?', ('%' + search_query + '%',))
        rows = cursor.fetchall()
        cursor.close()

        # Convert rows to list of dictionaries
        rows = [{'id': row[0], 'folder_name': row[1], 'metadata': row[2]} for row in rows]

        return config.jsonify(rows)

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
    return config.jsonify(rows)


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

    return config.redirect(config.url_for('index'))


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
