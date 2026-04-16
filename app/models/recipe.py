from . import get_db_connection
import sqlite3

class Recipe:
    """提供針對 Recipe 資料表的資料庫操作"""

    @staticmethod
    def create(title, ingredients, steps, image_url, user_id):
        """
        新增一篇食譜。
        
        Args:
            title (str): 食譜名稱
            ingredients (str): 食材清單
            steps (str): 製作步驟
            image_url (str): 圖片 URL (可選)
            user_id (int): 作者的使用者 ID
            
        Returns:
            int/None: 成功回傳新食譜的 ID，發生錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipe (title, ingredients, steps, image_url, user_id) VALUES (?, ?, ?, ?, ?)',
                (title, ingredients, steps, image_url, user_id)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in Recipe.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        透過 ID 取得單一食譜。
        
        Args:
            recipe_id (int): 食譜 ID
            
        Returns:
            dict/None: 成功回傳食譜字典，找不到或錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            recipe = conn.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()
            return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_by_id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有食譜清單，依建立時間由新到舊排序。
        
        Returns:
            list: 包含本站所有食譜字典的清單
        """
        conn = get_db_connection()
        try:
            recipes = conn.execute('SELECT * FROM recipe ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_all: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得指定使用者的所有食譜清單。
        
        Args:
            user_id (int): 使用者 ID
            
        Returns:
            list: 該使用者擁有的食譜清單
        """
        conn = get_db_connection()
        try:
            recipes = conn.execute('SELECT * FROM recipe WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            return [dict(row) for row in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_by_user_id: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def search_by_title_or_ingredient(keyword):
        """
        根據關鍵字搜尋食譜標題或食材清單。
        
        Args:
            keyword (str): 欲搜尋的關鍵字
            
        Returns:
            list: 符合條件的食譜清單
        """
        conn = get_db_connection()
        try:
            like_keyword = f"%{keyword}%"
            recipes = conn.execute(
                'SELECT * FROM recipe WHERE title LIKE ? OR ingredients LIKE ? ORDER BY created_at DESC',
                (like_keyword, like_keyword)
            ).fetchall()
            return [dict(row) for row in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.search_by_title_or_ingredient: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(recipe_id, title, ingredients, steps, image_url):
        """
        更新指定的食譜。
        
        Args:
            recipe_id (int): 欲更新的食譜 ID
            title (str): 食譜名稱
            ingredients (str): 食材清單
            steps (str): 製作步驟
            image_url (str): 圖片 URL (可選)
            
        Returns:
            bool: 成功回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE recipe SET title = ?, ingredients = ?, steps = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (title, ingredients, steps, image_url, recipe_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除指定的食譜。
        
        Args:
            recipe_id (int): 食譜 ID
            
        Returns:
            bool: 成功回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.delete: {e}")
            return False
        finally:
            conn.close()
