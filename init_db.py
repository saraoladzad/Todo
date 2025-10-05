import sqlite3


conn = sqlite3.connect('todo.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
