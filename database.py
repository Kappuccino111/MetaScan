from config import local_storage, sqlite3

def get_db():
    """Connect to the database through SQLite."""
    
    if not hasattr(local_storage, 'db'):
        local_storage.db = sqlite3.connect('image_database.db')
        local_storage.db.execute('PRAGMA foreign_keys = ON')  # Enable referential integrity
    return local_storage.db


def create_table():
    """Create a datbase table if it doesn't exist."""
    
    database = get_db()
    database.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT,
            metadata TEXT
        )
    ''')
    database.commit()

