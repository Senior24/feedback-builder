import sqlite3

class Database:
    def __init__(self, db_path: str = "database.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def add_user(self, user_id: int) -> None:
        with self.connection:
            self.connection.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def check_user(self, user_id: int) -> bool:
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return bool(self.cursor.fetchone())

    def add_bot(self, user_id: int, token: str) -> None:
        with self.connection:
            self.connection.execute("INSERT INTO bots (owner_id, token) VALUES (?,?)", (user_id, token))

    def check_bot(self, token: str) -> bool:
        with self.connection:
            self.cursor.execute("SELECT * FROM bots WHERE token = ?", (token,))
            return bool(self.cursor.fetchone())

    def bots_count(self, user_id: int) -> int:
        with self.connection:
            self.cursor.execute("SELECT * FROM bots WHERE owner_id = ?", (user_id,))
            return len(self.cursor.fetchall())

    def tokens_list(self) -> list[str]:
        with self.connection:
            self.cursor.execute("SELECT token FROM bots")
            rows = self.cursor.fetchall()
            tokens = [row[0] for row in rows]

            return tokens

db = Database()
