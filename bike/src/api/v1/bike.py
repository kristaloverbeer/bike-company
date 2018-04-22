from typing import Optional

from flask import request, make_response, jsonify, Blueprint
from flask_cors import CORS

from src.database.schemas.bike_schema import BikeSchema
from src.logging.mixin import LoggingMixin
from src.repository.bike_repository import BikeRepository

logger = LoggingMixin().logger

bike_blueprint = Blueprint('bike_blueprint', __name__, url_prefix='/v1')
CORS(bike_blueprint)


@bike_blueprint.route('/bikes', methods=['GET', 'POST'], defaults={'bike_id': None})
@bike_blueprint.route('/bikes/<bike_id>', methods=['GET'])
def bikes(bike_id: Optional[str]=None):
    bike_schema = BikeSchema()
    bikes_repository = BikeRepository(bike_schema)

    if request.method == 'POST':
        bikes_to_add = request.get_json()
        logger.debug('Received {} records to insert'.format(len(bikes_to_add)))

        message, status = bikes_repository.insert(bikes_to_add)
        return make_response(jsonify(message), status)

    elif request.method == 'GET':
        queried_bikes, status = bikes_repository.get(bike_id)
        return make_response(jsonify(queried_bikes), status)
