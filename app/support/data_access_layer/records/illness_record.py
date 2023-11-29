from datetime import datetime, timezone
from typing import Dict, Union
from decimal import Decimal

from app.support.data_access_layer.records.abstract_record import AbstractRecordFactory
from app.support.data_access_layer.records.pet_table_models import (
    IllnessRecordModel,
    RecordType
)
from app.support.common.misc import utc_timestamp_now


class IllnessRecordFactory(AbstractRecordFactory):
    model: IllnessRecordModel

    def __init__(self):
        self.model = IllnessRecordModel

    def produce_record(
            self,
            pet_name: str,
            ailment: str,
            observed_time: datetime,
            description: str
            ) -> Dict[str, Union[str, Decimal]]:
        sort_key = f"{RecordType.ILLNESS.value}#{ailment}#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "ailment": ailment,
            "date_time": Decimal(observed_time.astimezone(tz=timezone.utc).timestamp()),
            "description": description,
            'record_type': RecordType.ILLNESS.value
        }
        return illness_record
