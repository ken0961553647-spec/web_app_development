from . import get_db_connection
import sqlite3

class User:
    """提供針對 User 資料表的資料庫操作"""

    @staticmethod
    def create(username, email, password_hash):
        """
        新增一位使用者。
        
        Args:
            username (str): 使用者名稱
            email (str): 電子郵件
            password_hash (str): 加密後的密碼
            
        Returns:
            int/None: 成功回傳新使用者的 ID，失敗回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in User.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        透過 ID 取得單一使用者紀錄。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            dict/None: 成功回傳使用者字典，找不到或發生錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """
        透過使用者名稱取得單一使用者紀錄。
        
        Args:
            username (str): 使用者名稱
            
        Returns:
            dict/None: 成功回傳使用者字典，找不到或錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_username: {e}")
            return None
        finally:
            conn.close()
            
    @staticmethod
    def get_by_email(email):
        """
        透過電子郵件取得單一使用者紀錄。
        
        Args:
            email (str): 電子郵件
            
        Returns:
            dict/None: 成功回傳使用者字典，找不到或錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_email: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update_password(user_id, new_password_hash):
        """
        更新使用者的密碼。
        
        Args:
            user_id (int): 使用者 ID
            new_password_hash (str): 新的密碼 hash
            
        Returns:
            bool: 成功回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE user SET password_hash = ? WHERE id = ?',
                (new_password_hash, user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.update_password: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除使用者。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            bool: 成功回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM user WHERE id = ?', (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in User.delete: {e}")
            return False
        finally:
            conn.close()
