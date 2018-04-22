from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.database.models.bike import Bike


class BikeSchema(Schema):
    id = fields.String(required=True, allow_none=False)
    status = fields.Integer(required=False, allow_none=True)
    location = fields.Dict(required=True, allow_none=False)

    @post_load
    def make_bike(self, bike_data: dict) -> Bike:
        return Bike(**bike_data)

    @validates('location')
    def validate_location(self, location: dict) -> None:
        LOCATION_TYPES = ['Point']

        if 'type' not in location:
            raise ValidationError('Location data needs a type key')
        if location['type'] not in LOCATION_TYPES:
            raise ValidationError('Location type should be: {}'.format(', '.join(LOCATION_TYPES)))

        if 'coordinates' not in location:
            raise ValidationError('Location data needs coordinates')
        if not isinstance(location['coordinates'], list) or len(location['coordinates']) != 2:
            raise ValidationError('Coordinates should be a list of 2 elements')
