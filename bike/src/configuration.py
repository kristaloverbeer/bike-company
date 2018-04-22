import os

from src.logging.mixin import LoggingMixin


class Configuration(LoggingMixin):
    def __init__(self):
        self.logger.info('[SETUP] Configuration')
        self.database_uri = 'postgresql://{}:{}@{}:{}/{}'.format(
            os.environ.get('POSTGRES_USER'),
            os.environ.get('POSTGRES_PASSWORD'),
            os.environ.get('POSTGRES_HOST'),
            os.environ.get('POSTGRES_PORT'),
            os.environ.get('POSTGRES_DB'),
        )
        self.logger.info('[DONE] Configuration')
