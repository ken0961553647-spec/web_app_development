from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps
from . import recipes_bp
from app.models.recipe import Recipe
from app.models.tag import Tag

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行操作', 'error')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

@recipes_bp.route('/', methods=['GET'])
def list_recipes():
    """根據狀態顯示已登入使用者的食譜，或未登入時的公開首頁列表"""
    if 'user_id' in session:
        recipes = Recipe.get_by_user_id(session['user_id'])
    else:
        recipes = Recipe.get_all()
    return render_template('recipes/list.html', recipes=recipes)

@recipes_bp.route('/recipes/search', methods=['GET'])
def search_recipes():
    """根據 URL 的關鍵字搜尋食譜並渲染列表頁面"""
    q = request.args.get('q', '').strip()
    if q:
        recipes = Recipe.search_by_title_or_ingredient(q)
    else:
        recipes = Recipe.get_all()
    return render_template('recipes/list.html', recipes=recipes, search_query=q)

@recipes_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """顯示單篇食譜詳細內容與圖文步驟"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipes.list_recipes'))
    
    tags = Tag.get_by_recipe_id(id)
    return render_template('recipes/detail.html', recipe=recipe, tags=tags)

@recipes_bp.route('/recipes/new', methods=['GET'])
@login_required
def new_recipe_page():
    """顯示新增食譜的空白表單頁面"""
    return render_template('recipes/form.html', action='new')

@recipes_bp.route('/recipes/new', methods=['POST'])
@login_required
def create_recipe():
    """接收新增表單資料，寫入資料庫，並導向首頁"""
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    image_url = request.form.get('image_url')
    tags_input = request.form.get('tags', '') # 標籤以逗號分隔

    if not title or not ingredients or not steps:
        flash('請填寫所有必填欄位', 'error')
        return render_template('recipes/form.html', action='new', data=request.form)

    recipe_id = Recipe.create(title, ingredients, steps, image_url, session['user_id'])
    if recipe_id:
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag_id = Tag.create(name)
                if tag_id:
                    Tag.add_tag_to_recipe(recipe_id, tag_id)
        flash('食譜建立成功！', 'success')
        return redirect(url_for('recipes.list_recipes'))
    else:
        flash('建立失敗，請確認資料是否正確', 'error')
        return render_template('recipes/form.html', action='new', data=request.form)

@recipes_bp.route('/recipes/<int:id>/edit', methods=['GET'])
@login_required
def edit_recipe_page(id):
    """顯示帶有現有資料的食譜編輯表單"""
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限編輯此食譜', 'error')
        return redirect(url_for('recipes.list_recipes'))
    
    tags = Tag.get_by_recipe_id(id)
    tag_names = ', '.join([t['name'] for t in tags])
    
    recipe_data = dict(recipe)
    recipe_data['tags'] = tag_names

    return render_template('recipes/form.html', action='edit', data=recipe_data, recipe_id=id)

@recipes_bp.route('/recipes/<int:id>/edit', methods=['POST'])
@login_required
def update_recipe(id):
    """接收編輯表單資料，更新該筆食譜，並導向食譜詳情頁面"""
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限編輯此食譜', 'error')
        return redirect(url_for('recipes.list_recipes'))

    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    image_url = request.form.get('image_url')
    
    if not title or not ingredients or not steps:
        flash('請填寫所有必填欄位', 'error')
        return render_template('recipes/form.html', action='edit', data=request.form, recipe_id=id)

    success = Recipe.update(id, title, ingredients, steps, image_url)
    if success:
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.recipe_detail', id=id))
    else:
        flash('更新失敗，請稍後再試', 'error')
        return render_template('recipes/form.html', action='edit', data=request.form, recipe_id=id)

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    """驗證後刪除指定食譜，成功後導向首頁"""
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限刪除此食譜', 'error')
        return redirect(url_for('recipes.list_recipes'))

    success = Recipe.delete(id)
    if success:
        flash('已成功刪除食譜', 'success')
    else:
        flash('刪除失敗，請檢查權限或連線', 'error')
    return redirect(url_for('recipes.list_recipes'))
