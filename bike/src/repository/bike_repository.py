from typing import Optional, Union, List, Tuple

from src.database.models.bike import Bike, db
from src.logging.mixin import LoggingMixin


class BikeRepository(LoggingMixin):
    def __init__(self, bike_schema):
        self.bike_schema = bike_schema

    def insert(self, bikes_to_add: list) -> Tuple[dict, int]:
        self.logger.debug('Inserting {} bike records to database'.format(len(bikes_to_add)))

        deserialized_bikes, errors = self.bike_schema.load(bikes_to_add, many=True)
        if errors:
            return errors, 400
        for deserialized_bike in deserialized_bikes:
            db.session.add(deserialized_bike)
        db.session.commit()

        return {'message': 'Success'}, 201

    def get(self, bike_id: Optional[str]=None) -> Tuple[Union[dict, List[dict]], int]:
        if bike_id is not None:
            deserialized_bike = Bike.query.get_or_404(bike_id)
            serialized_bike, errors = self.bike_schema.dump(deserialized_bike)
            if errors:
                return errors, 400
            return serialized_bike, 200
        else:
            deserialized_bikes = Bike.query.all()
            serialized_bikes, errors = self.bike_schema.dump(deserialized_bikes, many=True)
            if errors:
                return errors, 400
            return serialized_bikes, 200
