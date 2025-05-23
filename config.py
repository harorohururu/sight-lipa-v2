import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_12345'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost/sight-v2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
