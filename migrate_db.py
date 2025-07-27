import sqlite3
import os
import datetime

# Path to the SQLite database
db_path = os.path.join('instance', 'portfolio.db')

# Check if database exists
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the created_at column already exists
cursor.execute("PRAGMA table_info(experience)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

if 'created_at' not in column_names:
    print("Adding created_at column to experience table...")
    try:
        # SQLite doesn't support DEFAULT CURRENT_TIMESTAMP in ALTER TABLE
        # So we need to add the column first, then update existing rows
        cursor.execute("ALTER TABLE experience ADD COLUMN created_at TEXT")
        
        # Set current timestamp for all existing rows
        current_time = datetime.datetime.now().isoformat()
        cursor.execute("UPDATE experience SET created_at = ?", (current_time,))
        
        conn.commit()
        print("Migration successful: created_at column added to experience table")
    except sqlite3.Error as e:
        print(f"Error during migration: {e}")
        conn.rollback()
else:
    print("created_at column already exists in experience table")

# Close the connection
conn.close()

print("Database migration completed")