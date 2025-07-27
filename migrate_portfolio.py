import sqlite3
import os
import json

# Path to the SQLite database
db_path = os.path.join('instance', 'portfolio.db')

# Check if database exists
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get current columns in the portfolio table
cursor.execute("PRAGMA table_info(portfolio)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# Add missing columns if they don't exist
try:
    # Start a transaction
    conn.execute("BEGIN TRANSACTION")
    
    # Add contact_info column (JSON)
    if 'contact_info' not in column_names:
        print("Adding contact_info column to portfolio table...")
        cursor.execute("ALTER TABLE portfolio ADD COLUMN contact_info TEXT")
        # Initialize with empty JSON object
        cursor.execute("UPDATE portfolio SET contact_info = ?",(json.dumps({}),))
    
    # Add skills column (JSON)
    if 'skills' not in column_names:
        print("Adding skills column to portfolio table...")
        cursor.execute("ALTER TABLE portfolio ADD COLUMN skills TEXT")
        # Initialize with empty JSON object
        cursor.execute("UPDATE portfolio SET skills = ?",(json.dumps({}),))
    
    # Add theme column with default 'professional'
    if 'theme' not in column_names:
        print("Adding theme column to portfolio table...")
        cursor.execute("ALTER TABLE portfolio ADD COLUMN theme TEXT DEFAULT 'professional'")
        cursor.execute("UPDATE portfolio SET theme = 'professional' WHERE theme IS NULL")
    
    # Commit the transaction
    conn.commit()
    print("Migration successful: Added missing columns to portfolio table")
    
except sqlite3.Error as e:
    print(f"Error during migration: {e}")
    conn.rollback()

# Close the connection
conn.close()

print("Portfolio table migration completed")