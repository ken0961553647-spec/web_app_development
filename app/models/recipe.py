from . import get_db_connection

class Recipe:
    @staticmethod
    def create(title, ingredients, steps, image_url, user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipe (title, ingredients, steps, image_url, user_id) VALUES (?, ?, ?, ?, ?)',
                (title, ingredients, steps, image_url, user_id)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        try:
            recipe = conn.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()
            return dict(recipe) if recipe else None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            recipes = conn.execute('SELECT * FROM recipe ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in recipes]
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        try:
            recipes = conn.execute('SELECT * FROM recipe WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            return [dict(row) for row in recipes]
        finally:
            conn.close()

    @staticmethod
    def search_by_title_or_ingredient(keyword):
        conn = get_db_connection()
        try:
            like_keyword = f"%{keyword}%"
            recipes = conn.execute(
                'SELECT * FROM recipe WHERE title LIKE ? OR ingredients LIKE ? ORDER BY created_at DESC',
                (like_keyword, like_keyword)
            ).fetchall()
            return [dict(row) for row in recipes]
        finally:
            conn.close()

    @staticmethod
    def update(recipe_id, title, ingredients, steps, image_url):
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE recipe SET title = ?, ingredients = ?, steps = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (title, ingredients, steps, image_url, recipe_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
            conn.commit()
        finally:
            conn.close()
