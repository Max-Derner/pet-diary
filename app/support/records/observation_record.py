from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.pet_table_models import (
    ObservationRecordModel,
    RecordType
)
from datetime import datetime, timezone
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
        sort_key = f"{RecordType.OBSERVATION.value}#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(observed_time.astimezone(tz=timezone.utc).timestamp()),  # noqa: E501
            "description": description,
            'record_type': RecordType.OBSERVATION.value
        }
        return illness_record
