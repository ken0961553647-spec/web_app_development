from . import get_db_connection

class Tag:
    @staticmethod
    def create(name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tag (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid
        except Exception:
            # 標籤若已存在，我們回傳現有的標籤 ID
            cursor = conn.execute('SELECT id FROM tag WHERE name = ?', (name,))
            row = cursor.fetchone()
            return row['id'] if row else None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            tags = conn.execute('SELECT * FROM tag ORDER BY name').fetchall()
            return [dict(row) for row in tags]
        finally:
            conn.close()

    @staticmethod
    def get_by_recipe_id(recipe_id):
        conn = get_db_connection()
        try:
            tags = conn.execute('''
                SELECT t.* FROM tag t
                JOIN recipe_tag rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            return [dict(row) for row in tags]
        finally:
            conn.close()

    @staticmethod
    def add_tag_to_recipe(recipe_id, tag_id):
        conn = get_db_connection()
        try:
            conn.execute('INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def remove_tag_from_recipe(recipe_id, tag_id):
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM recipe_tag WHERE recipe_id = ? AND tag_id = ?', (recipe_id, tag_id))
            conn.commit()
        finally:
            conn.close()
