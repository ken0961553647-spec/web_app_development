from . import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()
            
    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()

    @staticmethod
    def update_password(user_id, new_password_hash):
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE user SET password_hash = ? WHERE id = ?',
                (new_password_hash, user_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM user WHERE id = ?', (user_id,))
            conn.commit()
        finally:
            conn.close()
