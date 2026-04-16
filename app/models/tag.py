from . import get_db_connection
import sqlite3

class Tag:
    """提供針對 Tag 與中介表 Recipe_Tag 的資料庫操作"""

    @staticmethod
    def create(name):
        """
        新增一個標籤。若標籤已存在則回傳現有標籤 ID。
        
        Args:
            name (str): 標籤名稱
            
        Returns:
            int/None: 成功新增或已存在的標籤 ID，錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tag (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # 標籤名稱為 UNIQUE，若已存在則拋出 IntegrityError
            try:
                cursor = conn.execute('SELECT id FROM tag WHERE name = ?', (name,))
                row = cursor.fetchone()
                return row['id'] if row else None
            except Exception as e:
                print(f"Database error in Tag.create catch block: {e}")
                return None
        except sqlite3.Error as e:
            print(f"Database error in Tag.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有的標籤。
        
        Returns:
            list: 所有標籤字詞的清單
        """
        conn = get_db_connection()
        try:
            tags = conn.execute('SELECT * FROM tag ORDER BY name').fetchall()
            return [dict(row) for row in tags]
        except sqlite3.Error as e:
            print(f"Database error in Tag.get_all: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_recipe_id(recipe_id):
        """
        取得關聯至特定食譜的所有標籤。
        
        Args:
            recipe_id (int): 食譜 ID
            
        Returns:
            list: 該食譜附帶的標籤清單
        """
        conn = get_db_connection()
        try:
            tags = conn.execute('''
                SELECT t.* FROM tag t
                JOIN recipe_tag rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            return [dict(row) for row in tags]
        except sqlite3.Error as e:
            print(f"Database error in Tag.get_by_recipe_id: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def add_tag_to_recipe(recipe_id, tag_id):
        """
        將指定標籤綁定至指定食譜。
        
        Args:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID
            
        Returns:
            bool: 成功或已綁定回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            # 使用 INSERT OR IGNORE 避免重複關聯報錯
            conn.execute('INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Tag.add_tag_to_recipe: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def remove_tag_from_recipe(recipe_id, tag_id):
        """
        解除食譜與特定標籤的關聯。
        
        Args:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID
            
        Returns:
            bool: 成功解除回傳 True，否則回傳 False
        """
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM recipe_tag WHERE recipe_id = ? AND tag_id = ?', (recipe_id, tag_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Tag.remove_tag_from_recipe: {e}")
            return False
        finally:
            conn.close()
