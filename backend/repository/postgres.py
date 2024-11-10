from .entities import Repository
import psycopg2


class PostgresRepository(Repository):
    def __init__(self, db_string):
        self.db_string = db_string
        self.conn = psycopg2.connect(self.db_string)
        self._create_game_table()

    def _create_game_table(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game (
                game_id TEXT PRIMARY KEY,
                password TEXT,
                attempts INTEGER
            )
        ''')
        conn.commit()

    def store(self, game_id, data: dict):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game (game_id, password, attempts)
            VALUES (%s, %s, %s)
        ''', (game_id, data["password"], 0))
        conn.commit()

    def retrieve(self, game_id):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute('''
            SELECT game_id, password, attempts
            FROM game
            WHERE game_id = %s
        ''', (game_id,))
        result = cursor.fetchone()

        if result:
            game_id, password, attempts = result
            return {"password": password, "attempts": attempts}
        return None
