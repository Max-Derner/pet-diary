from app.support.records.pet_table_models import IllnessRecordModel
from app.support.records.abstract_record import AbstractRecordFactory
from datetime import datetime
from typing import Dict, Union
from support.misc import utc_timestamp_now
from decimal import Decimal


class IllnessRecordFactory(AbstractRecordFactory):
    model: IllnessRecordModel

    def __init__(self):
        self.model = IllnessRecordModel

    def produce_record(
            self,
            name: str,
            ailment: str,
            date_time: datetime,
            description: str
            ) -> Dict[str, Union[str, Decimal]]:
        sort_key = f"illness#{ailment}#{utc_timestamp_now()}"
        illness_record = {
            "name": name,
            "sort_key": sort_key,
            "ailment": ailment,
            "date_time": Decimal(date_time.timestamp()),
            "description": description
        }
        return illness_record