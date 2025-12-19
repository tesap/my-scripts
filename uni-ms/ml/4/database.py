import sqlite3
import json

import sqlite3

def get_value_by_id(db_path, record_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM main WHERE id = ?", (record_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    DB = "2.db"
    value = get_value_by_id(DB, 1)
    print(f"Value for ID 1: {value}")
    
    # Get value with ID 10 (non-existent)
    value = get_value_by_id(DB, 10)
    print(f"Value for ID 10: {value}")  # Should print "None"
        
