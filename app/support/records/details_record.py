from typing import Dict, Union
from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.pet_table_models import DetailsRecordModel
from datetime import datetime
from decimal import Decimal


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
    ) -> Dict[str, Union[str, Decimal, int]]:
        details_record = {
            "name": name,
            "sort_key": "details",
            "dob": Decimal(date_of_birth.timestamp()),
            "colour": colour,
            "gender": gender,
            "breed": breed,
            "microchip_number": microchip_number
        }
        return details_record
