from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊頁面表單"""
    pass

@auth_bp.route('/register', methods=['POST'])
def register():
    """接收註冊表單，寫入資料庫並導向登入頁"""
    pass

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入頁面表單"""
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    """驗證登入帳密，成功儲存 session 並導向首頁"""
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """清除 session 並導向首頁"""
    pass
