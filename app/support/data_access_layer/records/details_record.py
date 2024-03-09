from typing import Dict, Union
from datetime import datetime
from decimal import Decimal

from app.support.data_access_layer.records.abstract_record import AbstractRecordFactory
from app.support.data_access_layer.records.pet_table_models import (
    DetailsRecordModel,
    RecordType
)
from app.support.common.misc import utc_timestamp_now


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
            'date_time': Decimal(utc_timestamp_now()),
            "colour": colour,
            "gender": gender,
            "breed": breed,
            "microchip_number": Decimal(microchip_number),
            'record_type': RecordType.DETAILS.value
        }
        return details_record
