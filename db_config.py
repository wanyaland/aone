import os

if os.environ.get('ENVIRONMENT', 'DEV') == 'DEV':
    os.environ['DB_NAME'] = 'africaone'
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASSWORD'] = 'root'
    os.environ['DB_HOST'] = '127.0.0.1'
    os.environ['DB_PORT'] = '3306'
