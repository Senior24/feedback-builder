import json
import sqlite3

class Database:
    def __init__(self, db_path: str = "database.db"):
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
            pro     INTEGER DEFAULT (0) NOT NULL
            );""")

            self.connection.execute("""CREATE TABLE IF NOT EXISTS bots (
            owner_id        INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
            token           TEXT    UNIQUE,
            admins          TEXT,
            welcome_message TEXT
            );""")

    def add_user(self, user_id: int):
        with self.connection:
            self.connection.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def check_user(self, user_id: int) -> bool:
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return bool(self.cursor.fetchone())

    def add_bot(self, user_id: int, token: str):
        with self.connection:
            self.connection.execute("INSERT INTO bots (owner_id, token) VALUES (?,?)", (user_id, token))

    def remove_bot(self, token: str):
        with self.connection:
            self.connection.execute("DELETE FROM bots WHERE token = ?", (token,))

    def check_bot(self, token: str) -> bool:
        with self.connection:
            self.cursor.execute("SELECT * FROM bots WHERE token = ?", (token,))
            return bool(self.cursor.fetchone())

    def admin(self, user_id: int, token: str, add: bool = False, remove: bool = False):
        with self.connection:
            self.cursor.execute("SELECT admins FROM bots WHERE token = ?", (token,))
            result = self.cursor.fetchone()[0]
            admins = json.loads(result) if result else []

            if add:
                admins.append(user_id)
            if remove:
                admins.remove(user_id)

            self.connection.execute("UPDATE bots SET admins = ? WHERE token = ?", (json.dumps(admins), token))

    def admins_list(self, token: str, with_owner: bool = True) -> list[int]:
        with self.connection:
            self.cursor.execute("SELECT owner_id FROM bots WHERE token = ?", (token,))
            owner_id = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT admins FROM bots WHERE token = ?", (token,))
            result = self.cursor.fetchone()[0]
            admins = json.loads(result) if result else []

            if with_owner:
                admins.append(owner_id)

            return admins

    def give_pro(self, user_id: int):
        with self.connection:
            self.connection.execute("UPDATE users SET pro = ? WHERE user_id = ?", (1, user_id))

    def check_pro(self, user_id: int) -> bool:
        with self.connection:
            self.cursor.execute("SELECT pro FROM users WHERE user_id = ?", (user_id,))
            return bool(self.cursor.fetchone()[0])

    def bots_count(self, user_id: int) -> int:
        with self.connection:
            self.cursor.execute("SELECT * FROM bots WHERE owner_id = ?", (user_id,))
            return len(self.cursor.fetchall())

    def tokens_list(self, user_id: int = None) -> list[str]:
        with self.connection:
            if user_id:
                self.cursor.execute('SELECT token FROM bots WHERE owner_id = ?', (user_id,))
            else:
                self.cursor.execute("SELECT token FROM bots")

            rows = self.cursor.fetchall()
            tokens = [row[0] for row in rows]

            return tokens

    def set_welcome_message(self, message: str, token: str):
        with self.connection:
            self.connection.execute("UPDATE bots SET welcome_message = ? WHERE token = ?", (message, token))

    def get_welcome_message(self, token: str) -> str | None:
        with self.connection:
            self.cursor.execute("SELECT welcome_message FROM bots WHERE token = ?", (token,))
            return self.cursor.fetchone()[0]


db = Database()
