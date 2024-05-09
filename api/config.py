import os

APP_ENV = os.getenv('APP_ENV', 'development')

DATABASE_USERNAME = os.getenv('DATABASE_USER_NAME', 'halodb')

# DATABASE_HOST = os.getenv('DATABASE_HOST', 'db')
# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'HaloDBat2024.')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'halodb')

DATABASE_PORT = os.getenv('DATABASE_PORT', 3306)
DATABASE_NAME = os.getenv('DATABASE_NAME', 'halodb')
