from typing import Dict, Union
from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.pet_table_models import (
    DetailsRecordModel,
    RecordType
)
from datetime import datetime
from decimal import Decimal


class DetailsRecordFactory(AbstractRecordFactory):
    model: DetailsRecordModel

    def __init__(self):
        self.model = DetailsRecordModel

    def produce_record(
            self,
            pet_name: str,
            date_of_birth: datetime,
            colour: str,
            gender: str,
            breed: str,
            microchip_number: int
    ) -> Dict[str, Union[str, Decimal]]:
        details_record = {
            "name": pet_name,
            "sort_key": RecordType.DETAILS.value,
            "dob": Decimal(date_of_birth.timestamp()),
            "colour": colour,
            "gender": gender,
            "breed": breed,
            "microchip_number": Decimal(microchip_number),
            'record_type': RecordType.DETAILS.value
        }
        return details_record

    def _extra_record_validation(self, record: Dict) -> bool:
        try:
            # Dynamo requires all numbers are Decimal,
            # this needs to be natural number
            int(record['microchip_number'])
        except ValueError:
            return False
        return True
