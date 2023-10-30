from app.support.records.pet_table_models import ObservationRecordModel
from app.support.records.abstract_record import AbstractRecordFactory
from datetime import datetime
from typing import Dict, Union
from app.support.misc import utc_timestamp_now
from decimal import Decimal


class ObservationRecordFactory(AbstractRecordFactory):
    model: ObservationRecordModel

    def __init__(self):
        self.model = ObservationRecordModel

    def produce_record(
            self,
            pet_name: str,
            observed_time: datetime,
            description: str
            ) -> Dict[str, Union[str, Decimal]]:
        sort_key = f"observation#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(observed_time.timestamp()),
            "description": description
        }
        return illness_record
