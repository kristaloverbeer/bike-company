import os
from typing import Optional

import requests
from flask import Blueprint, Response, request
from flask_cors import CORS

from src.logging.mixin import LoggingMixin

logger = LoggingMixin().logger

gateway_blueprint = Blueprint('gateway_blueprint', __name__, url_prefix='/v1')
CORS(gateway_blueprint)


@gateway_blueprint.route('/bikes', methods=['GET'], defaults={'bike_id': None})
@gateway_blueprint.route('/bikes/<bike_id>', methods=['GET'])
def get_bikes(bike_id: Optional[str] = None) -> Response:
    logger.debug('Calling bike service to list bikes')
    url_to_request = '{}/v1/bikes'.format(os.environ.get('BIKE_SERVICE'))
    if bike_id is not None:
        url_to_request += '/{}'.format(bike_id)
    with requests.sessions.Session() as session:
        response = session.request(
            method=request.method,
            url=url_to_request,
            headers=request.headers,
        )

    headers = [
        (name, value)
        for (name, value)
        in response.raw.headers.items()
    ]
    return Response(response.content, response.status_code, headers)


@gateway_blueprint.route('/trips/start/<bike_id>', methods=['PUT'])
def start_trip(bike_id: str) -> Response:
    logger.debug('Calling trip service to start trip')
    url_to_request = '{}/v1/trips/start/{}'.format(os.environ.get('TRIP_SERVICE'), bike_id)
    with requests.sessions.Session() as session:
        response = session.request(
            method=request.method,
            url=url_to_request,
            headers=request.headers,
        )

    headers = [
        (name, value)
        for (name, value)
        in response.raw.headers.items()
    ]
    return Response(response.content, response.status_code, headers)


@gateway_blueprint.route('/trips/end/<bike_id>', methods=['PATCH'])
def end_trip(bike_id: str) -> Response:
    logger.debug('Calling trip service to end trip')
    url_to_request = '{}/v1/trips/end/{}'.format(os.environ.get('TRIP_SERVICE'), bike_id)
    with requests.sessions.Session() as session:
        response = session.request(
            method=request.method,
            url=url_to_request,
            headers=request.headers,
        )

    headers = [
        (name, value)
        for (name, value)
        in response.raw.headers.items()
    ]
    return Response(response.content, response.status_code, headers)
