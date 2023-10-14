import sqlite3

class DniModel:
    def read_all(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()
        return data
    

    def create_user(self, username, email):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))


    def update_user(self, user_id, new_username, new_email):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username=?, email=? WHERE id=?", (new_username, new_email, user_id))

    def delete_user(self, user_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    def get_user_by_id(self, user_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = cursor.fetchone()
            return user if user else None