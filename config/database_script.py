import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Crea una tabla para usuarios
cursor.execute("CREATE TABLE users_dni (dni INTEGER PRIMARY KEY, nombre TEXT, apellido_pat TEXT, apellido_mat TEXT)")

conn.commit()
conn.close()