import os
from base64 import b64encode
from dotenv import load_dotenv


class Config(object):
    """Parent Configuration Class"""
    env_file = os.path.abspath('.') + '/.env'
    key = b64encode(os.urandom(32)).decode('utf-8')

    with open(env_file, 'r') as file:
        env_data = file.readlines()

    for line_number, line in enumerate(env_data):
        if line.startswith('APP_KEY='):
            env_data[line_number] = 'APP_KEY={0}\n'.format(key)
            break

    with open(env_file, 'w') as file:
        file.writelines(env_data)

    load_dotenv(env_file)

    DB_DATABASE = os.getenv('DB_DATABASE')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PORT = int(os.getenv('DB_PORT'))

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('APP_KEY')

    POSTGRES_INTERNAL = f'{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
    SQLALCHEMY_DATABASE_URI = f"postgres+psycopg2://" + POSTGRES_INTERNAL
    SQLALCHEMY_BINDS = {'readonly': f"postgres+psycopg2://" + POSTGRES_INTERNAL}

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = True

    # celery configurations
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_DB_NO, REDIS_HOST, REDIS_PORT = 0, os.getenv("REDIS_HOST"), int(os.getenv("REDIS_PORT"))

    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    SESSION_WITH_REDIS = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_NO, "password": REDIS_PASSWORD}


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DB_DATABASE = "test_db"
    POSTGRES_INTERNAL = f'{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:' \
        f'{os.getenv("DB_PORT")}/{DB_DATABASE}'
    SQLALCHEMY_DATABASE_URI = f"postgresql://" + POSTGRES_INTERNAL
    SQLALCHEMY_BINDS = {'readonly': f"postgresql://" + POSTGRES_INTERNAL}
    DEBUG = True


class StagingConfig(Config):
    """Configuration for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}


def app_configuration(app):
    """
    Set up Configuration
    @param app:
    """
    APP_STATUS = os.getenv('APP_ENV')
    UPLOADS = os.path.join(os.getcwd(), 'storage/uploads')

    if APP_STATUS == 'testing':
        app.config.from_object('core.config.TestingConfig')
    elif APP_STATUS == 'staging':
        app.config.from_object('core.config.StagingConfig')
    elif APP_STATUS == 'production':
        app.config.from_object('core.config.ProductionConfig')
    else:
        app.config.from_object('core.config.DevelopmentConfig')

    # create non existent uploads directory
    if not os.path.exists(UPLOADS):
        try:
            os.mkdir(UPLOADS)
        except (Exception,):
            pass

    app.jinja_env.cache = {}  # hasten the loading of templates
    app.jinja_env.trim_blocks = True  # Removes unwanted whitespace from render_template function
