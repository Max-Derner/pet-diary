from datetime import datetime, timezone
from typing import Dict
from decimal import Decimal

from app.support.data_access_layer.records.abstract_record import AbstractRecordFactory
from app.support.data_access_layer.records.pet_table_models import (
    ObservationRecordModel,
    RecordType
)
from app.support.common.misc import utc_timestamp_now


class ObservationRecordFactory(AbstractRecordFactory):
    model: ObservationRecordModel

    def __init__(self):
        self.model = ObservationRecordModel

    def produce_record(
            self,
            pet_name: str,
            observed_time: datetime,
            description: str
            ) -> Dict[str, str | Decimal]:
        sort_key = f"{RecordType.OBSERVATION.value}#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(observed_time.astimezone(tz=timezone.utc).timestamp()),
            "description": description,
            'record_type': RecordType.OBSERVATION.value
        }
        return illness_record
