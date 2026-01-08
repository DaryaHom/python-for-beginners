"""
Flask application for subscription tracking and analysis.

This module contains route handlers for:
- managing subscriptions (CRUD);
- displaying subscription list;
- performing financial analysis over a selected period.

The application uses:
- Flask for web routing;
- WTForms for form validation;
- PostgreSQL storage;
- pandas-based analytics.
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
