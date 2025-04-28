"""
Simple script to view SQLite database contents.
"""
import sqlite3
import os

def view_tables():
    """Display all tables in the database."""
    conn = sqlite3.connect('biz4ai.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if not tables:
        print("No tables found in the database.")
        return
    
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
    
    # For each table, show data
    for table in tables:
        table_name = table[0]
        print(f"\nContents of table '{table_name}':")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print("| " + " | ".join(column_names) + " |")
        print("| " + " | ".join(["---" for _ in column_names]) + " |")
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found.")
        else:
            for row in rows:
                print("| " + " | ".join([str(cell) for cell in row]) + " |")
    
    conn.close()

if __name__ == "__main__":
    view_tables()
