from typing import List

from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.database.models.trip import Trip


class TripSchema(Schema):
    id = fields.String(required=True, allow_none=False)
    status = fields.Integer(required=False, allow_none=True)
    bike_id = fields.String(required=True, allow_none=False)
    locations = fields.List(fields.Dict(), required=False, allow_none=True)
    started_at = fields.DateTime(required=False, allow_none=True)
    ended_at = fields.DateTime(required=False, allow_none=True)

    @post_load
    def make_trip(self, trip_data: dict) -> Trip:
        return Trip(**trip_data)

    @validates('locations')
    def validate_locations(self, locations: List[dict]) -> None:
        LOCATION_TYPES = ['Point']
        for location in locations:
            if 'type' not in location:
                raise ValidationError('Location data needs a type key')
            if location['type'] not in LOCATION_TYPES:
                raise ValidationError('Location type should be: {}'.format(', '.join(LOCATION_TYPES)))

            if 'coordinates' not in location:
                raise ValidationError('Location data needs coordinates')
            if not isinstance(location['coordinates'], list) or len(location['coordinates']) != 2:
                raise ValidationError('Coordinates should be a list of 2 elements')
