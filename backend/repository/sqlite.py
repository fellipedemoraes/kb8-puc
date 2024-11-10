from .entities import Repository
import sqlite3


class SQLiteRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_game_table()

    def _create_game_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game (
                game_id TEXT PRIMARY KEY,
                password TEXT,
                attempts INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def store(self, game_id, data: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game (game_id, password, attempts)
            VALUES (?, ?, ?)
        ''', (game_id, data["password"], 0))
        conn.commit()
        conn.close()

    def retrieve(self, game_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT game_id, password, attempts
            FROM game
            WHERE game_id = ?
        ''', (game_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            game_id, password, attempts = result
            return {"password": password, "attempts": attempts}
        return None
