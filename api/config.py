import os
from typing import Optional


def get_secret(var: str, file_var: str, default: Optional[str]) -> Optional[str]:
    """
    try os.getenv(var) first, otherwise read from os.getenv(file_var)
    """
    value = os.getenv(var)

    if value is not None:
        return value

    file = os.getenv(file_var)

    if file is None:
        return default

    exists = os.path.exists(file)

    if exists:
        return open(file).read().rstrip('\n')

    return default


APP_ENV = os.getenv('APP_ENV', 'development')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')

MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'halodb')

MYSQL_USER = os.getenv('MYSQL_USER_NAME', 'halodb')
MYSQL_PASSWORD = get_secret('MYSQL_PASSWORD', 'MYSQL_PASSWORD_FILE', 'halodb')

UPLOADS_DIR = os.getenv('UPLOADS_DIR', './uploads')
