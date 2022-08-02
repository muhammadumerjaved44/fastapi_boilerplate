from decouple import config


TEMP_ENV = config("ENV")


class Config:
    """Base config."""

    pass

    PROJECT_NAME = config("PROJECT_NAME") + "_APi"


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


class TestConfig(Config):
    ENV = "testing"
    DEBUG = False


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False


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
