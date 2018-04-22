import datetime
import uuid
from typing import Tuple

import requests
from sqlalchemy import desc

from src.configuration import Configuration
from src.database.models.trip import Trip, db
from src.logging.mixin import LoggingMixin


class TripRepository(LoggingMixin):
    def __init__(self, trip_schema):
        self.trip_schema = trip_schema
        # TODO: proper injection of this dependance in the repository init
        self.configuration = Configuration()

    def start_trip(self, bike_id: str) -> Tuple[dict, int]:
        self.logger.debug('Starting trip for bike {}'.format(bike_id))
        formatted_bike_url = '{}/v1/bikes/{}'.format(self.configuration.bike_service, bike_id)
        bike_request = requests.get(formatted_bike_url)
        if 200 <= bike_request.status_code < 300:
            bike = bike_request.json()
        else:
            return {'message': 'Requested bike does not exist'}, 400

        trip_to_add = {
            'id': uuid.uuid4().hex[:20],
            'bike_id': bike_id,
            'status': 1,
            'locations': [bike['location']],
        }

        deserialized_trip, errors = self.trip_schema.load(trip_to_add)
        if errors:
            return errors, 400
        db.session.add(deserialized_trip)
        db.session.commit()

        return {'id': trip_to_add['id']}, 201

    def end_trip(self, bike_id: str) -> Tuple[dict, int]:
        self.logger.debug('Ending trip for bike {}'.format(bike_id))
        # TODO: need to update the new endpoint location of the bike
        deserialized_bike = self._get_bike_last_trip(bike_id)
        deserialized_bike.status = 0
        deserialized_bike.ended_at = datetime.datetime.utcnow()
        db.session.commit()

        serialized_bike, errors = self.trip_schema.dump(deserialized_bike)
        if errors:
            return errors, 400

        return serialized_bike, 200

    def in_use(self, bike_id: str) -> bool:
        deserialized_trip = self._get_bike_last_trip(bike_id)
        if deserialized_trip is not None:
            if deserialized_trip.status == 1:
                return True
        return False

    def _get_bike_last_trip(self, bike_id):
        bike_last_trip = Trip.query \
            .filter_by(bike_id=bike_id) \
            .order_by(desc(Trip.started_at)) \
            .first()
        return bike_last_trip
