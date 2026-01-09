"""
Приложение для трекинга подписочных сервисов и аналитики расходов

Приложение использует:
- Flask для web-роутинга;
- WTForms для валидации форм;
- PostgreSQL хранилище;
- pandas для построения аналитики.
"""
from app import app
from config import SERVER_CONFIG

if __name__ == "__main__":
    app.config['SECRET_KEY'] = SERVER_CONFIG['secret_key']
    app.run(
        host=SERVER_CONFIG['host'], 
        port=SERVER_CONFIG['port'], 
        debug=SERVER_CONFIG['debug'],
    )
