import os
import sqlite3
from datetime import datetime, timedelta



class Database:
    def __init__(self, db_file):
        # Исправленный путь для Linux (уберите префикс C:\ для Windows)
        self.db_path = os.path.abspath(db_file.replace('C:\\', '/mnt/c/').replace('\\', '/'))
        print(f"[DEBUG] Путь к БД: {self.db_path}")

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    phone TEXT,
                     join_date TIMESTAMP NULL
                )
            ''')

    def add_user(self, user_id, username, first_name, phone, join_date=None):
        with self.conn:
            self.conn.execute(
                'INSERT INTO users (user_id, username, first_name, phone, join_date) VALUES (?, ?, ?, ?, ?)',
                (user_id, username, first_name, phone, join_date)
            )
            self.conn.commit()

    def get_users(self):
        with self.conn:
            return self.conn.execute('SELECT * FROM users').fetchall()

    def remove_expired_users(self):
        month_ago = datetime.now() - timedelta(days=30)
        formatted_date = month_ago.strftime('%Y-%m-%d %H:%M:%S')

        with self.conn:
            # Для отладки
            old_users = self.conn.execute(
                'SELECT * FROM users WHERE datetime(join_date) < datetime(?)',
                (formatted_date,)
            ).fetchall()
            print(f"Удаляемые пользователи: {old_users}")

            # Удаление
            cursor = self.conn.execute(
                'DELETE FROM users WHERE datetime(join_date) < datetime(?)',
                (formatted_date,)
            )
            self.conn.commit()
            return cursor.rowcount

    def remove_user_by_id(self, user_id):
        with self.conn:
            cursor = self.conn.execute(
                'DELETE FROM users WHERE user_id = ?',
                (user_id,)
            )
            self.conn.commit()
            return cursor.rowcount
    def get_chat_id_by_phone(self, phone):
        with self.conn:
            result = self.conn.execute('SELECT user_id FROM users WHERE phone = ?', (phone,))
            row = result.fetchone()
            return row[0] if row else None

    def get_phone_by_id(self, user_id):
        with self.conn:
            result = self.conn.execute('SELECT phone FROM users WHERE user_id = ?', (user_id,))
            row = result.fetchone()
            return row[0] if row else None

    def set_join_date(self, user_id, join_date=None):
        """Обновляет дату присоединения для пользователя по user_id"""
        if join_date is None:
            join_date = datetime.now()
        with self.conn:
            self.conn.execute(
                'UPDATE users SET join_date = ? WHERE user_id = ?',
                (join_date, user_id)
            )
            self.conn.commit()

db = Database('../users.db')