import sqlite3

# Use the same DB Alembic migrations run on
conn = sqlite3.connect("D:/E-Commerce/E-Commerce/E-Commerce.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(search_index);")
for row in cursor.fetchall():
    print(row)

conn.close()