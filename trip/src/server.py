from flask import Flask
from flask_migrate import Migrate

from src.api.index import index_blueprint
from src.api.ping import ping_blueprint
from src.api.v1.trip import trip_blueprint
from src.configuration import Configuration
from src.database.models.trip import db
from src.logging.mixin import LoggingMixin

logger = LoggingMixin().logger


def create_api(configuration: Configuration) -> Flask:
    logger.info('[SETUP] API Application')

    api = Flask(__name__)

    api.url_map.strict_slashes = False
    api.config['SQLALCHEMY_DATABASE_URI'] = configuration.database_uri
    api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    _register_blueprints(api)

    logger.info('[DONE] API Application')
    return api


def _register_blueprints(api_application: Flask) -> None:
    api_application.register_blueprint(ping_blueprint)
    api_application.register_blueprint(index_blueprint)
    api_application.register_blueprint(trip_blueprint)


configuration = Configuration()
api = create_api(configuration)
db.init_app(api)
migration = Migrate(api, db)
