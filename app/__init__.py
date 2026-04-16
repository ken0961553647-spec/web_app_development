from flask import Flask
from config import Config
import os
import sqlite3

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)

    # 註冊 Blueprints
    from app.routes import auth_bp, recipes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)

    return app

def init_db():
    """初始化資料庫工具函式"""
    app = create_app()
    with app.app_context():
        db_path = app.config['DATABASE_PATH']
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print('Database initialized.')
