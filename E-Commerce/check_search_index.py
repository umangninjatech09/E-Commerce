import sqlite3

# Connect to the correct database
conn = sqlite3.connect("E-Commerce.db")
cursor = conn.cursor()

# Use the actual table name, not the file name
cursor.execute("PRAGMA table_info(search_index);")
for row in cursor.fetchall():
    print(row)

conn.close()
