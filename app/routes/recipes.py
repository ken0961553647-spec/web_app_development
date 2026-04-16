from flask import render_template, request, redirect, url_for, flash, session
from . import recipes_bp

@recipes_bp.route('/', methods=['GET'])
def list_recipes():
    """根據登入狀態顯示首頁內容或使用者的食譜列表"""
    pass

@recipes_bp.route('/recipes/search', methods=['GET'])
def search_recipes():
    """根據 URL 的關鍵字搜尋食譜並渲染列表頁面"""
    pass

@recipes_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """顯示單篇食譜詳細內容與圖文步驟"""
    pass

@recipes_bp.route('/recipes/new', methods=['GET'])
def new_recipe_page():
    """顯示新增食譜的空白表單頁面"""
    pass

@recipes_bp.route('/recipes/new', methods=['POST'])
def create_recipe():
    """接收新增表單資料，寫入資料庫，並導向首頁"""
    pass

@recipes_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe_page(id):
    """顯示帶有現有資料的食譜編輯表單"""
    pass

@recipes_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """接收編輯表單資料，更新該筆食譜，並導向食譜詳情頁面"""
    pass

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """驗證後刪除指定食譜，成功後導向首頁"""
    pass
