import os
import sqlite3
from app.core.config import settings

def reset_vector_index():
    index_path = settings.VECTOR_INDEX_PATH
    vector_file = os.path.join(index_path, "vectors.npy")
    metadata_file = os.path.join(index_path, "metadata.json")

    files_to_remove = [vector_file, metadata_file]

    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
        else:
            print(f"File not found: {file}")

    print("Vector index has been reset.")

def reset_main_database():
    # Extract the SQLite database file path from the DATABASE_URL
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Function to execute SQL and print results
    def execute_and_print(sql):
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"{sql} -> {result[0] if result else 'N/A'}")

    # Count records before deletion
    print("Counts before deletion:")
    execute_and_print("SELECT COUNT(*) FROM chunks")
    execute_and_print("SELECT COUNT(*) FROM documents")
    execute_and_print("SELECT COUNT(*) FROM libraries")

    # Delete records
    cursor.execute("DELETE FROM chunks")
    cursor.execute("DELETE FROM documents")
    cursor.execute("DELETE FROM libraries")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('chunks', 'documents', 'libraries')")
    conn.commit()

    print("\nRecords deleted.")

    # Count records after deletion
    print("\nCounts after deletion:")
    execute_and_print("SELECT COUNT(*) FROM chunks")
    execute_and_print("SELECT COUNT(*) FROM documents")
    execute_and_print("SELECT COUNT(*) FROM libraries")

    # Close the connection
    conn.close()

    print("Main database has been reset.")

if __name__ == "__main__":
    reset_vector_index()
    reset_main_database()