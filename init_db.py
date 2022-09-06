import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO players (player, score) VALUES (?, ?)", ('Luan', '0'))

cur.execute("INSERT INTO players (player, score) VALUES (?, ?)", ('Nathan', '0'))

connection.commit()
connection.close()
