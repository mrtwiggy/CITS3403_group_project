"""
Database connection test script.
Run this to check if your database connection is working properly.
"""

import os
import sqlite3
from my_app import create_app
from my_app.config import DeploymentConfig

app = create_app(DeploymentConfig)

with app.app_context():
    # Get the database URI from the app config
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"Database URI: {db_uri}")
    
    # If it's a SQLite URI, extract the path
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri[10:]  # Remove 'sqlite:///'
        print(f"SQLite database path: {db_path}")
        
        # Check if the path exists
        db_dir = os.path.dirname(db_path)
        print(f"Database directory: {db_dir}")
        print(f"Directory exists: {os.path.exists(db_dir)}")
        print(f"Directory is writable: {os.access(db_dir, os.W_OK)}")
        
        # Try to open the database file
        try:
            conn = sqlite3.connect(db_path)
            print("Successfully connected to the database!")
            conn.close()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    else:
        print("Not a SQLite database URI")

print("\nPossible issues and solutions:")
print("1. Directory doesn't exist: Create it manually or check permissions")
print("2. Directory not writable: Change permissions with chmod")
print("3. Path issues: Make sure the path is correct and absolute")

if __name__ == "__main__":
    print("\nRun this script with:")
    print("python db_debug.py")