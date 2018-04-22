from typing import Optional

from flask import make_response, jsonify, Blueprint, Response
from flask_cors import CORS

from src.database.schemas.trip_schema import TripSchema
from src.logging.mixin import LoggingMixin
from src.repository.trip_repository import TripRepository

logger = LoggingMixin().logger

trip_blueprint = Blueprint('trip_blueprint', __name__, url_prefix='/v1')
CORS(trip_blueprint)


@trip_blueprint.route('/trips/start/<bike_id>', methods=['PUT'])
def start_trip(bike_id: str) -> Response:
    trip_schema = TripSchema()
    trips_repository = TripRepository(trip_schema)

    logger.debug('Trip to start with bike: {}'.format(bike_id))

    bike_already_in_use = trips_repository.in_use(bike_id)

    if not bike_already_in_use:
        message, status = trips_repository.start_trip(bike_id)
        return make_response(jsonify(message), status)

    else:
        return make_response(jsonify({'message': 'Bike already in use'}), 200)


@trip_blueprint.route('/trips/end/<bike_id>', methods=['PATCH'])
def end_trip(bike_id: str) -> Response:
    trip_schema = TripSchema()
    trips_repository = TripRepository(trip_schema)

    logger.debug('Trip to end with bike: {}'.format(bike_id))

    bike_already_in_use = trips_repository.in_use(bike_id)

    if bike_already_in_use:
        message, status = trips_repository.end_trip(bike_id)
        return make_response(jsonify(message), status)
    else:
        return make_response(jsonify({'message': 'Current bike is not in use'}), 200)
