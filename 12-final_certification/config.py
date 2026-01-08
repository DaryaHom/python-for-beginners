import os
import secrets

DB_CONFIG = {
    'database': os.getenv('DB_NAME', 'subscriptions'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
}

SERVER_CONFIG = {
    'host': os.getenv('APP_HOST', 'localhost'),
    'port': os.getenv('APP_PORT', 8081),
    'secret_key': os.getenv('APP_SECRET_KEY', secrets.token_urlsafe(32)),
    'debug': True,
}
