import os

class Config:
    # 從環境變數取得 SECRET_KEY，否則使用預設值
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    # 設定資料庫路徑
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
