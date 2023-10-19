from typing import Dict, Union
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.pet_table_models import DetailsRecordModel  # noqa: E501
from datetime import datetime


class DetailsRecordFactory(AbstractRecordFactory):
    model: DetailsRecordModel

    def __init__(self):
        self.model = DetailsRecordModel

    def produce_record(
            self,
            name: str,
            date_of_birth: datetime,
            colour: str,
            gender: str,
            breed: str,
            microchip_number: int
    ) -> Dict[str, Union[str, float, int]]:
        details_record = {
            "name": name,
            "sort_key": "details",
            "dob": date_of_birth.timestamp(),
            "colour": colour,
            "gender": gender,
            "breed": breed,
            "microchip_number": microchip_number
        }
        return details_record
