from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.pet_table_models import (
    IllnessRecordModel,
    RecordType
)
from datetime import datetime, timezone
from typing import Dict, Union
from support.misc import utc_timestamp_now
from decimal import Decimal


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
        sort_key = f"{RecordType.ILLNESS.value}#{ailment}#{utc_timestamp_now()}"  # noqa: E501
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "ailment": ailment,
            "date_time": Decimal(observed_time.astimezone(tz=timezone.utc).timestamp()),  # noqa: E501
            "description": description,
            'record_type': RecordType.ILLNESS.value
        }
        return illness_record
