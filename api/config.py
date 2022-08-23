from decouple import config
from pydantic import AnyHttpUrl
import json
from typing import List

TEMP_ENV = config("ENV")


class Config:
    """Base config."""

    PROJECT_NAME = config("PROJECT_NAME") + "_API"


class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    DB_DRIVER = config("DB_DRIVER")
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT", cast=int)
    DATABASE_NAME = config("DATABASE_NAME")
    API_PORT_DOCKER = config("API_PORT_DOCKER", cast=int)
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    SECRET_KEY = config("SECRET_KEY")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = json.loads(config("BACKEND_CORS_ORIGINS"))
    STELLO_EMAIL = config("STELLO_EMAIL")
    SENDGRID_API_KEY = config("SENDGRID_API_KEY")
    S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
    S3_CSV_BUCKET = config("S3_CSV_BUCKET")
    S3_CSV_FOLDER = config("S3_CSV_FOLDER")
    FIRST_SUPERUSER_EMAIL = config("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD")
    TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE_NUMBER = config("TWILIO_FROM_PHONE_NUMBER")
    TWILIO_TO_PHONE_NUMBER = config("TWILIO_TO_PHONE_NUMBER")


class TestConfig(Config):
    ENV = "testing"
    DEBUG = True
    DB_DRIVER = config("DB_DRIVER")
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT", cast=int)
    DATABASE_NAME = config("DATABASE_NAME")
    API_PORT_DOCKER = config("API_PORT_DOCKER", cast=int)
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    SECRET_KEY = config("SECRET_KEY")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = json.loads(config("BACKEND_CORS_ORIGINS"))
    STELLO_EMAIL = config("STELLO_EMAIL")
    SENDGRID_API_KEY = config("SENDGRID_API_KEY")
    S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
    S3_CSV_BUCKET = config("S3_CSV_BUCKET")
    S3_CSV_FOLDER = config("S3_CSV_FOLDER")
    FIRST_SUPERUSER_EMAIL = config("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD")
    TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE_NUMBER = config("TWILIO_FROM_PHONE_NUMBER")
    TWILIO_TO_PHONE_NUMBER = config("TWILIO_TO_PHONE_NUMBER")


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False
    DB_DRIVER = config("DB_DRIVER")
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT", cast=int)
    DATABASE_NAME = config("DATABASE_NAME")
    API_PORT_DOCKER = config("API_PORT_DOCKER", cast=int)
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    SECRET_KEY = config("SECRET_KEY")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = json.loads(config("BACKEND_CORS_ORIGINS"))
    STELLO_EMAIL = config("STELLO_EMAIL")
    SENDGRID_API_KEY = config("SENDGRID_API_KEY")
    S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
    S3_CSV_BUCKET = config("S3_CSV_BUCKET")
    S3_CSV_FOLDER = config("S3_CSV_FOLDER")
    FIRST_SUPERUSER_EMAIL = config("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD")
    TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE_NUMBER = config("TWILIO_FROM_PHONE_NUMBER")


def get_settings():
    if TEMP_ENV == "development":
        settings = DevConfig()
        return settings
    elif TEMP_ENV == "testing":
        settings = TestConfig()
        return settings
    elif TEMP_ENV == "production":
        settings = ProdConfig()
        return settings
    else:
        raise Exception("Invalid  ENV environment variable value")


settings = get_settings()
