from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊頁面表單"""
    return render_template('auth/register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    """接收註冊表單，寫入資料庫並導向登入頁"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash('請填寫所有必填欄位', 'error')
        return redirect(url_for('auth.register_page'))

    if User.get_by_username(username):
        flash('該使用者名稱已被使用', 'error')
        return redirect(url_for('auth.register_page'))
        
    if User.get_by_email(email):
        flash('該信箱已被註冊', 'error')
        return redirect(url_for('auth.register_page'))

    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)

    user_id = User.create(username, email, password_hash)
    if user_id:
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('註冊失敗，請稍後再試', 'error')
        return redirect(url_for('auth.register_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入頁面表單"""
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    """驗證登入帳密，成功儲存 session 並導向首頁"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('請填寫信箱與密碼', 'error')
        return redirect(url_for('auth.login_page'))

    user = User.get_by_email(email)
    from werkzeug.security import check_password_hash
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('登入成功！', 'success')
        return redirect(url_for('recipes.list_recipes'))
    else:
        flash('信箱或密碼錯誤', 'error')
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """清除 session 並導向首頁"""
    session.clear()
    flash('您已登出', 'info')
    return redirect(url_for('recipes.list_recipes'))
