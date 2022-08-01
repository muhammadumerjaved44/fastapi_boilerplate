from decouple import config


TEMP_ENV = config("ENV")


class Config:
    """Base config."""

    pass

    PROJECT_NAME = config("PROJECT_NAME") + "_APi"


class DevConfig(Config):
    ENV = "development"


class TestConfig(Config):
    ENV = "testing"


class ProdConfig(Config):
    ENV = "production"


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
